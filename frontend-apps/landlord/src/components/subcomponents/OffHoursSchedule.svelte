<script>
// @ts-nocheck


export let boiler;

import {
    message,
    messenger,
} from '../../stores/store';
import axios from 'axios';
import Select from 'svelte-select';
import RangeSlider from "svelte-range-slider-pips";;
import { slide, scale, fade } from 'svelte/transition';
import { quintOut } from "svelte/easing";
import { onMount } from 'svelte';
import { getCsrfCookieValue } from '../../lib/utils';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();


const time_options = {timeZone: 'UTC', hour: '2-digit', minute:'2-digit'}

let schedule_options = [];
let weekdays_edit_form = false;
let weekend_edit_form = false;

let weekdays_offhours_start_time = boiler.data.weekdays_offhours_start_time;
let weekdays_offhours_end_time = boiler.data.weekdays_offhours_end_time;
let weekdays_offhours_enabled = boiler.data.weekdays_offhours_enabled;
let weekdays_offhours_setpoint = boiler.data.weekdays_offhours_setpoint;

let weekend_offhours_start_time = boiler.data.weekend_offhours_start_time;
let weekend_offhours_end_time = boiler.data.weekend_offhours_end_time;
let weekend_offhours_enabled = boiler.data.weekend_offhours_enabled;
let weekend_offhours_setpoint = boiler.data.weekend_offhours_setpoint;

onMount(async () => {
    await loadScheduleOptions();
})

async function loadScheduleOptions() {
    try {
        const endpoint = `/api/schedules/options/1/`;

        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
            // console.log("Options", response.data)
            schedule_options = response.data.map(
                x => new Object(
                    {value: new Date(x.checkpoint).toISOString().substring(11,19), label: new Date(x.checkpoint).toLocaleTimeString('en-US', time_options)}
                    ))
            }
            const schedule_options_a = schedule_options.filter(x => parseInt(x.value.substring(0,5).replace(":", "")) >= 1200)
            const schedule_options_b = schedule_options.filter(x => parseInt(x.value.substring(0,5).replace(":", "")) < 1200)
            schedule_options_a.sort((a, b) => (parseInt(a.value.substring(0,5).replace(":", "")) > parseInt(b.value.substring(0,5).replace(":", ""))) ? 1 : -1)
            schedule_options_b.sort((a, b) => (parseInt(a.value.substring(0,5).replace(":", "")) > parseInt(b.value.substring(0,5).replace(":", ""))) ? 1 : -1)
            schedule_options = schedule_options_a.concat(schedule_options_b)

           // schedule_options.sort((a, b) => (parseInt(a.value.substring(0,5).replace(":", "")) > parseInt(b.value.substring(0,5).replace(":", ""))) ? 1 : -1)
            // console.log("schedule_options", schedule_options)
    } catch(error) {
            console.log(error)
    }
}


async function saveSettings(data = {}) {


//   const validation = validateForm();
//   if (!validation) return;
   
  try {
  const endpoint = `/api/devices/boiler/${boiler.data.id}/`;
  const csrfcookie = getCsrfCookieValue();

  const response = await axios({
      url: endpoint,
      method: "patch",
      data: data,
      headers: {
        'X-CSRFToken': csrfcookie
      }

  });
  if(response.status === 200) {

            weekdays_offhours_start_time = response.data.weekdays_offhours_start_time;
            weekdays_offhours_end_time = response.data.weekdays_offhours_end_time;
            weekdays_offhours_enabled = response.data.weekdays_offhours_enabled;
            weekdays_offhours_setpoint = response.data.weekdays_offhours_setpoint;

            weekend_offhours_start_time = response.data.weekend_offhours_start_time;
            weekend_offhours_end_time = response.data.weekend_offhours_end_time;
            weekend_offhours_enabled = response.data.weekend_offhours_enabled;
            weekend_offhours_setpoint = response.data.weekend_offhours_setpoint;
            $message =  "Off-hours schedule was successfully updated"
            $messenger = true;

      }
  } catch(error) {
          console.log(error)
          $message =  "Something went wrong 🤖. Please, try again later."
          $messenger = true;
  }
};

function toggleEvent(type) {
    if (type === 0) {
        weekdays_offhours_enabled = !weekdays_offhours_enabled;
        const data = {
            "weekdays_offhours_enabled": weekdays_offhours_enabled
        }
        saveSettings(data);
        
    }
    if (type === 1) {
        weekend_offhours_enabled = !weekend_offhours_enabled;
        const data = {
            "weekend_offhours_enabled": weekend_offhours_enabled
        }
        saveSettings(data);
        
    }
}

function closeSchedulePopup() {
    dispatch('close');
}

function handleWeekdaysOffHoursRange(e) {
    if (e.detail.activeHandle === 0) {
        weekdays_offhours_start_time = schedule_options[e.detail.value].value
        const data = {
            'weekdays_offhours_start_time': weekdays_offhours_start_time
        }
        saveSettings(data);
    }
    if (e.detail.activeHandle === 1) {
        weekdays_offhours_end_time = schedule_options[e.detail.value].value
        const data = {
            'weekdays_offhours_end_time': weekdays_offhours_end_time
        }
        saveSettings(data);
    }
}
function handleWeekdaysSetpoint(e) {
    weekdays_offhours_setpoint = e.detail.value;
    const data = {
        'weekdays_offhours_setpoint': weekdays_offhours_setpoint,
    }
    saveSettings(data);
}


function handleWeekendOffHoursRange(e) {
    if (e.detail.activeHandle === 0) {
        weekend_offhours_start_time = schedule_options[e.detail.value].value
        const data = {
            'weekend_offhours_start_time': weekend_offhours_start_time
        }
        saveSettings(data);
    }
    if (e.detail.activeHandle === 1) {
        weekend_offhours_end_time = schedule_options[e.detail.value].value
        const data = {
            'weekend_offhours_end_time': weekend_offhours_end_time
        }
        saveSettings(data);
    }
}
function handleWeekendSetpoint(e) {
    weekend_offhours_setpoint = e.detail.value;
    const data = {
        'weekend_offhours_setpoint': weekend_offhours_setpoint,
    }
    saveSettings(data);
}

async function parseUSTime(timestamp) {
    if (schedule_options.length === 0) {
        await loadScheduleOptions();
    }
    const obj_list = schedule_options.filter(x => x.value === timestamp)
    if (obj_list.length === 1) {
        return obj_list[0].label
    } else return '--'
}
</script>

<div id="schedule-overlay" in:fade on:click|self={() => closeSchedulePopup()}
class="absolute left-0 top-0 w-full h-full flex flex-col flex-grow items-center cursor-pointer justify-center bg-black bg-opacity-30">
    <div transition:scale={{ delay: 250, duration: 300, easing: quintOut }} id="schedule-ui" class="flex flex-col w-full max-w-screen-md bg-white shadow-sm rounded-md px-8 py-8">
        <div class="flex flex-col">
            <div class="flex flex-row items-center">
                <div class="inline-flex flex-grow">
                    <button
                    class="btn-secondary text-sm px-4 py-2">
                       Off-hours schedule
                    </button>
                </div>
                <div class="inline-flex" on:click={() => closeSchedulePopup()}>
                    <svg class="fill-current w-6" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 135 135" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                        <g><polygon class="fil0" points="0,9 59,68 0,126 9,135 68,77 126,135 135,126 77,68 135,9 126,0 68,59 9,0 "></polygon></g>
                    </svg>
                </div>
            </div>
                <div class="py-4 mt-4 font-semibold">
                    Weekdays off-hours (Mon - Fri)
                </div>
                <div class="grid grid-cols-5 gap-2 pb-2 text-sm font-medium">
                    <div>
                        Start at
                    </div>
                    <div>
                        End at
                    </div>
                    <div>
                        Setpoint °F
                    </div>
                    <div>
                        Status
                    </div>
                    <div>
                        Action
                    </div>
                </div>
                <div class="grid grid-cols-5 gap-2 py-2 px-4 shadow-md rounded-md items-center bg-gradient-to-r from-gray-50 to-gray-200" 
                on:click={() => weekdays_edit_form = !weekdays_edit_form}>
                        <div>
                            {#await parseUSTime(weekdays_offhours_start_time)}
                                '--'
                            {:then value} 
                                {value}
                            {/await}
                        </div>
                        <div>
                            {#await parseUSTime(weekdays_offhours_end_time)}
                                '--'
                            {:then value} 
                                {value}
                            {/await}
                        </div>
                        <div>{weekdays_offhours_setpoint || '--'} °F</div>
                        <div>
                            {weekdays_offhours_enabled ? 'Active' : 'Disabled' }
                        </div>
                        <div on:click|stopPropagation={() => toggleEvent(0)} class="w-8 cursor-pointer">
                            <svg class="fill-current text-gray-400 transform transition-colors" class:text-green-500={weekdays_offhours_enabled===true}
                            x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
                            <title>{!weekdays_offhours_enabled ? 'Enabled' : 'Disabled'} </title>
                            <switch><g><path d="M50,2.5L50,2.5C23.8,2.5,2.5,23.8,2.5,50l0,0c0,26.2,21.3,47.5,47.5,47.5l0,0c26.2,0,47.5-21.3,47.5-47.5l0,0    C97.5,23.8,76.2,2.5,50,2.5z M45.7,24.2c0-2.4,1.9-4.3,4.3-4.3s4.3,1.9,4.3,4.3v21.6c0,2.4-1.9,4.3-4.3,4.3s-4.3-1.9-4.3-4.3V24.2    z M50,78.4c-15.2,0-27.6-12.4-27.6-27.6c0-8.7,4-16.7,11-22c1.9-1.4,4.6-1,6,0.8c1.4,1.9,1,4.6-0.8,6c-4.8,3.6-7.6,9.2-7.6,15.2    c0,10.5,8.5,19.1,19.1,19.1c10.5,0,19.1-8.5,19.1-19.1c0-6-2.8-11.5-7.6-15.2c-1.9-1.4-2.3-4.1-0.8-6c1.4-1.9,4.1-2.3,6-0.8    c7,5.3,11,13.3,11,22C77.6,66,65.2,78.4,50,78.4z"></path></g></switch></svg>      
                        </div>
                        <!-- <div on:click|stopPropagation={() => toggleEvent(0)}>
                            {#if !weekdays_offhours_enabled}
                            <button class="btn-tertiary text-sm px-4 py-1.5">
                                Enable
                            </button>
                            {:else}
                            <button class="btn-primary text-sm px-4 py-1.5">
                                Disable
                            </button>
                            {/if}
                        </div> -->
                </div>
                <!-- Weekdays edit form -->
                {#if weekdays_edit_form}
                <div class="px-5">
                    <div class="mt-2 pt-2">
                        Select start and end time
                    </div>
                    <div class="py-10">
                        <div>
                        <RangeSlider min={0} max={95} 
                        range={false}
                        values={[
                            schedule_options.findIndex(x => x.value === weekdays_offhours_start_time),
                            schedule_options.findIndex(x => x.value === weekdays_offhours_end_time),
                            ]}
                        handleFormatter={(v) => schedule_options[v].label }
                        formatter={(v,i,p) => schedule_options[v].label }
                        float={true}
                        pushy={false}
                        pips
                        pipstep={19}
                        all='label'
                        on:stop={(e) => handleWeekdaysOffHoursRange(e)}
                        disabled={!weekdays_offhours_enabled}
                        />
                        </div>
                    </div>
                    <div class="py-2">
                        Select thermostat setpoint
                    </div>
                    <div class="py-4 slider-theme" >
                        <RangeSlider min={40} max={90} 
                        force_float={true} float pips 
                        values={[weekdays_offhours_setpoint]}
                        formatter={(v) => v + ' °F' }
                        first='label'
                        last='label'
                        on:stop={(e) => handleWeekdaysSetpoint(e)} 
                        disabled={!weekdays_offhours_enabled}
                        />
                    </div>
                </div>
                {/if}

                <div class="py-4 mt-4 font-semibold">
                    Weekend off-hours (Sat - Sun)
                </div>
                <div class="grid grid-cols-5 gap-2 pb-2 px-5 text-sm font-medium">
                    <div>
                        Start at
                    </div>
                    <div>
                        End at
                    </div>
                    <div>
                        Setpoint °F
                    </div>
                    <div>
                        Status
                    </div>
                    <div>
                        Action
                    </div>
                </div>
                <div on:click={() => weekend_edit_form = !weekend_edit_form}
                class="grid grid-cols-5 gap-2 py-2 px-4 shadow-md rounded-md items-center bg-gradient-to-r from-gray-50 to-gray-200">
                    <div>
                        {#await parseUSTime(weekend_offhours_start_time)}
                            '--'
                        {:then value} 
                            {value}
                        {/await}
                    </div>
                    <div>
                        {#await parseUSTime(weekend_offhours_end_time)}
                            '--'
                        {:then value} 
                            {value}
                        {/await}
                    </div>
                    <div>{weekend_offhours_setpoint || '--'} °F</div>
                    <div>
                        {weekend_offhours_enabled ? 'Active' : 'Disabled' }
                    </div>
                    <div on:click|stopPropagation={() => toggleEvent(1)} class="w-8 cursor-pointer">
                        <svg class="fill-current text-gray-400 transform transition-colors" class:text-green-500={weekend_offhours_enabled===true}
                        x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
                        <title>{!weekend_offhours_enabled ? 'Enabled' : 'Disabled'} </title>
                        <switch><g><path d="M50,2.5L50,2.5C23.8,2.5,2.5,23.8,2.5,50l0,0c0,26.2,21.3,47.5,47.5,47.5l0,0c26.2,0,47.5-21.3,47.5-47.5l0,0    C97.5,23.8,76.2,2.5,50,2.5z M45.7,24.2c0-2.4,1.9-4.3,4.3-4.3s4.3,1.9,4.3,4.3v21.6c0,2.4-1.9,4.3-4.3,4.3s-4.3-1.9-4.3-4.3V24.2    z M50,78.4c-15.2,0-27.6-12.4-27.6-27.6c0-8.7,4-16.7,11-22c1.9-1.4,4.6-1,6,0.8c1.4,1.9,1,4.6-0.8,6c-4.8,3.6-7.6,9.2-7.6,15.2    c0,10.5,8.5,19.1,19.1,19.1c10.5,0,19.1-8.5,19.1-19.1c0-6-2.8-11.5-7.6-15.2c-1.9-1.4-2.3-4.1-0.8-6c1.4-1.9,4.1-2.3,6-0.8    c7,5.3,11,13.3,11,22C77.6,66,65.2,78.4,50,78.4z"></path></g></switch></svg>      
                    </div>
                </div>
                <!-- Weekend edit form -->
                {#if weekend_edit_form}
                <div class="px-5">
                    <div class="mt-2 pt-2">
                        Select start and end time
                    </div>
                    <div class="py-10">
                        <div>
                        <RangeSlider min={0} max={95} 
                        range={false}
                        values={[
                            schedule_options.findIndex(x => x.value === weekend_offhours_start_time),
                            schedule_options.findIndex(x => x.value === weekend_offhours_end_time),
                            ]}
                        handleFormatter={(v) => schedule_options[v].label }
                        formatter={(v,i,p) => schedule_options[v].label }
                        float={true}
                        pushy={false}
                        pips
                        pipstep={19}
                        all='label'
                        on:stop={(e) => handleWeekendOffHoursRange(e)}
                        disabled={!weekend_offhours_enabled}
                        />
                        </div>
                    </div>
                    <div class="py-2">
                        Select thermostat setpoint
                    </div>
                    <div class="py-4 slider-theme" >
                        <RangeSlider min={40} max={90} 
                        force_float={true} float pips 
                        values={[weekend_offhours_setpoint]}
                        formatter={(v) => v + ' °F' }
                        first='label'
                        last='label'
                        on:stop={(e) => handleWeekendSetpoint(e)} 
                        disabled={!weekend_offhours_enabled}
                        />
                    </div>
                </div>
                {/if}
            <div>
            </div>
        </div>
    </div>
</div>

<style>
    /* input:checked + label{
        box-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    } */
    #schedule-ui {
        z-index: 30;
    }
    #schedule-overlay {
        z-index: 20;
    }
</style>