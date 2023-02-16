<script>

export let device_type;
export let device_id;

import {
    message,
    messenger,
} from '../../stores/store';
import axios from 'axios';
import Select from 'svelte-select';
import RangeSlider from "svelte-range-slider-pips";
import { slide, scale, fade } from 'svelte/transition';
import { quintOut } from "svelte/easing";
import { onMount } from 'svelte';
import { getCsrfCookieValue } from '../../lib/utils';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

let events = [];
let schedule_options = [];

let new_event_form = false;
let new_event_weekday, new_event_timestamp_id;
let new_event_setpoint = 60;
let switch_state;

let state_options = [
    {value: true, label: 'Switch ON'},
    {value: false, label: 'Switch OFF'},
  ];

onMount(() => {
    loadEvents();
})

async function loadEvents() {

    const endpoint = `/api/schedules/tenant/${device_type}/?device_id=${device_id}`
    try {
        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
            events = response.data;
            }
            console.log("events", events)
    } catch(error) {
            console.log(error)
    }
}

async function loadScheduleOptions() {
    try {
        const endpoint = `/api/schedules/options/${new_event_weekday}/`;

        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
            // console.log("Options", response.data)
            // schedule_options = response.data.map(x => new Object({value: x.id, label: x.checkpoint.substring(11,16)}))
            schedule_options = response.data.map(
                x => new Object(
                    {value: x.id, label: new Date(x.checkpoint).toLocaleTimeString('en-US')}
                    ))
            }
    } catch(error) {
            console.log(error)
    }
    console.log("schedule_options", schedule_options)
}


async function deleteEvent(event_id) {
    try {
        const endpoint = `/api/schedules/tenant/${device_type}/delete/`;
        const csrfcookie = getCsrfCookieValue();
        const response = await axios({
            url: endpoint,
            method: "post",
            data: {
                "pk": event_id,
            },
            headers: {
            'X-CSRFToken': csrfcookie
            }
        });
        if(response.status === 204) {
            loadEvents();
            }
    } catch(error) {
            console.log(error)
    }
}


async function saveNewEvent() {
  
    try {
    const endpoint = `/api/schedules/tenant/${device_type}/create/`;
    const csrfcookie = getCsrfCookieValue();
    let data = {};
    if (device_type === 'thermostats') {
        data = {
            "schedule": new_event_timestamp_id,
            "thermostat": device_id,
            "setpoint": new_event_setpoint,
        }
    }
    if (device_type === 'switches') {
        data = {
            "schedule": new_event_timestamp_id,
            "switch": device_id,
            "status": switch_state,
        }
    }
    if (device_type === 'analogue-thermostats') {
        data = {
            "schedule": new_event_timestamp_id,
            "analogue_thermostat": device_id,
            "status": switch_state,
        }
    }
    const response = await axios({
        url: endpoint,
        method: "post",
        data: data,
        headers: {
          'X-CSRFToken': csrfcookie
        }

    });
    if(response.status === 201) {
            new_event_form = false;
            loadEvents();
            $message =  "New schedule event was successfully created."
            $messenger = true;
        }
    } catch(error) {
            console.log(error)
            $message =  "Something went wrong 🤖. Please, try again later."
            $messenger = true;
    }
};

function selectWeekDay(index) {
    new_event_weekday = index + 1;
    loadScheduleOptions();
}

function resetForm() {
    new_event_form = false;
    new_event_setpoint = 60;
    new_event_weekday = undefined;
    new_event_timestamp_id = undefined;
    switch_state = false;
}

function closeSchedulePopup() {
    dispatch('close');
}

function handleScheduleSelect(event) {
	new_event_timestamp_id = event.detail.value;
}

	
function handleScheduleClear() {
    new_event_timestamp_id = undefined;
}

function handleStateSelect(event) {
    switch_state = event.detail.value;
}

function handleStateClear(event) {
    switch_state = undefined;
}
</script>

<div id="schedule-overlay" in:fade on:click|self={() => closeSchedulePopup()}
class="absolute left-0 top-0 w-full h-full flex flex-col flex-grow items-center cursor-pointer justify-center bg-black bg-opacity-30">
    <div transition:scale={{ delay: 250, duration: 300, easing: quintOut }} id="schedule-ui" class="flex flex-col w-full max-w-screen-md bg-white shadow-sm rounded-md px-8 py-8">
        <div class="flex flex-col">
            <div class="flex flex-row items-center">
                <div class="inline-flex flex-grow">
                    <button on:click={()=> new_event_form =true}
                    class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">
                        Add new event
                    </button>
                </div>
                <div class="inline-flex" on:click={() => closeSchedulePopup()}>
                    <svg class="fill-current w-6" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 135 135" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                        <g><polygon class="fil0" points="0,9 59,68 0,126 9,135 68,77 126,135 135,126 77,68 135,9 126,0 68,59 9,0 "></polygon></g>
                    </svg>
                </div>
            </div>
            {#if new_event_form}
            <div in:slide out:fade class="flex flex-col mt-5">
                <div in:fade>
                    <div class="text-sm py-2">
                        1. Select the day of the week
                    </div>
                    <div class="flex flex-row flex-wrap gap-4 text-sm mt-4 py-2">
                        {#each weekdays as weekday, index }
                        <div>
                            <input type="radio" class="hidden" id="{index}" name="weekday">
                            <label on:click={() => selectWeekDay(index)}
                            for="{index}" class="bg-gray-100 text-center px-4 py-1 rounded-md text-black font-semibold cursor-pointer">
                                {weekday}
                            </label>
                        </div>
                        {/each}
                    </div>
                </div>
                
                {#if new_event_weekday }
                <div in:fade>
                    <div class="text-sm py-2 mt-4">
                        2. Select available time
                    </div>
                    <div class="mt-4 flex flex-col py-2 px-4 gap-y-3 bg-white max-w-sm">
                        <Select items={schedule_options} on:select={handleScheduleSelect} on:clear={handleScheduleClear}/>
                    </div>
                </div>
                {/if}
                {#if new_event_timestamp_id && device_type === 'thermostats'}
                <div in:fade>
                    <div class="text-sm py-2 mt-4">
                        3. Select setpoint for this thermostat
                    </div>
                    <div class="flex flex-col py-5">
                        <div class="slidecontainer mr-1 max-w-sm">
                            <RangeSlider min={40} max={90} force_float={true} float pips values={[new_event_setpoint]} on:stop={(e) => new_event_setpoint = e.detail.value} />
                        </div>
                        <!-- <div class="font-semibold">
                            {new_event_setpoint} °
                        </div> -->
                    </div>
                </div>
                {:else if new_event_timestamp_id }
                <div in:fade>
                    <div class="text-sm py-2 mt-4">
                        3. Choose an action
                    </div>
                    <div class="my-2 max-w-xs z-40 ml-4">
                        <Select items={state_options} placeholder="Which action to perform?" placeholderAlwaysShow={true}
                        on:select={handleStateSelect} on:clear={handleStateClear} />
                    </div>
                </div>
                {/if}
                <div class="flex flex-row gap-x-7 mt-4">
                    {#if new_event_timestamp_id}
                    <div>
                        <button on:click={() => saveNewEvent()}
                        class="ring-2 text-sm ring-green-400 rounded-md px-4 mt-4 py-1 active:ring-green-700">
                            Save
                        </button>
                    </div>
                    {/if}
                    <div>
                        <button on:click|self={() => resetForm() }
                        class="ring-2 text-sm ring-gray-300 rounded-md px-4 mt-4 py-1 active:ring-gray-700">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
            {/if}
        </div>
        <div class="py-4 text-lg mt-4 font-semibold">
            Scheduled events
        </div>
        {#if device_type === 'thermostats'}

            {#each events as event}
            <div class="grid grid-cols-4 mt-4 px-4 py-2 max-w-screen-md shadow-md bg-white rounded-md">
                <div>
                    {weekdays[event.schedule.week_day-1]}
                </div>
                <div>
                    {new Date(event.schedule.checkpoint).toLocaleTimeString('en-US')}
                </div>
                <div>
                    {event.setpoint} °
                </div>
                <div>
                    <button on:click={() => deleteEvent(event.id)}
                    class="ring-2 text-sm ring-green-200 rounded-md px-4 py-1 active:ring-green-700">
                        Remove
                    </button>
                </div>
            </div>
            {:else}
            <div class="grid grid-cols-4 gap-y-2 max-w-screen-md mt-2">
                <div class="col-span-4 text-sm">
                    You don't have any scheduled thermostat changes
                </div>
            </div>
            {/each}
        
        {:else}
            {#each events as event}
            <div in:slide class="grid grid-cols-4 max-w-screen-md mt-4 shadow-md rounded-md px-4 py-2">
                <div>
                    {weekdays[event.schedule.week_day-1]}
                </div>
                <div>
                    {event.schedule.checkpoint.substring(11,16)}
                </div>
                <div>
                    {event.status === true ? 'ON' : 'OFF'}
                </div>
                <div>
                    <button on:click={() => deleteEvent(event.id)}
                    class="ring-2 text-sm ring-green-200 rounded-md px-4 py-1 active:ring-green-700">
                        Remove
                    </button>
                </div>
            </div>
            {:else}
            <div in:slide class="grid grid-cols-4 max-w-screen-md mt-4 shadow-md rounded-md px-4 py-2">
                <div class="col-span-4 text-sm">
                    You don't have any scheduled thermostat changes
                </div>
            </div>
            {/each}
        
        {/if}
    </div>
</div>

<style>
    input:checked + label{
        box-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    }


    #schedule-ui {
        z-index: 101;
    }
    #schedule-overlay {
        z-index: 100;
    }
</style>