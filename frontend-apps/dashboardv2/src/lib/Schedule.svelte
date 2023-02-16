<script>
    export let thermostat;

    import axios from "axios";
    import Select from "svelte-select";
    import { slide, fade } from "svelte/transition";
    import { onMount } from "svelte";
    import { getCsrfCookieValue } from "../lib/utils";
    import { createEventDispatcher } from "svelte";
    import { toast } from "@zerodevx/svelte-toast";

    const dispatch = createEventDispatcher();

    const weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ];

    let events = [];
    let schedule_options = [];

    let new_event_form = false;
    let new_event_weekday, new_event_timestamp_id;
    let new_event_setpoint = 60;
    let switch_state;

    let state_options = [
        { value: true, label: "Switch ON" },
        { value: false, label: "Switch OFF" },
    ];

    onMount(() => {
        loadEvents();
    });

    async function loadEvents() {
        const endpoint = `/api/schedules/thermostats/?device_id=${thermostat.id}`;
        try {
            const response = await axios({
                url: endpoint,
                method: "get",
            });
            if (response.status === 200) {
                events = response.data;
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function loadScheduleOptions() {
        try {
            const endpoint = `/api/schedules/options/${new_event_weekday}/`;

            const response = await axios({
                url: endpoint,
                method: "get",
            });
            if (response.status === 200) {
                // console.log("Options", response.data)
                schedule_options = response.data.map(
                    (x) =>
                        new Object({
                            value: x.id,
                            label: x.checkpoint.substring(11, 16),
                        })
                );
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function deleteEvent(event_id) {
        try {
            const endpoint = `/api/schedules/thermostats/delete/`;
            const csrfcookie = getCsrfCookieValue();
            const response = await axios({
                url: endpoint,
                method: "post",
                data: {
                    pk: event_id,
                },
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (response.status === 204) {
                loadEvents();
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function saveNewEvent() {
        try {
            const endpoint = `/api/schedules/thermostats/create/`;
            const csrfcookie = getCsrfCookieValue();
            const data = {
                schedule: new_event_timestamp_id,
                thermostat: thermostat.id,
                setpoint: new_event_setpoint,
            };

            const response = await axios({
                url: endpoint,
                method: "post",
                data: data,
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (response.status === 201) {
                new_event_form = false;
                loadEvents();
                toast.push("New schedule event was successfully created.");
            }
        } catch (error) {
            console.log(error);
            toast.push("Something went wrong 🤖. Please, try again later.");
        }
    }

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
        dispatch("close");
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

<div class="pb-4">
    <div class="flex flex-col">
        <div class="flex flex-row items-center">
            <div class="inline-flex flex-grow">
                <button
                    on:click={() => (new_event_form = true)}
                    class="btn btn-primary btn-sm btn-wide"
                >
                    Add new event
                </button>
            </div>
            <button class="inline-flex" on:click={() => closeSchedulePopup()}>
                <svg
                    class="fill-current w-4"
                    xml:space="preserve"
                    version="1.1"
                    style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;"
                    viewBox="0 0 135 135"
                    x="0px"
                    y="0px"
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                >
                    <g
                        ><polygon
                            class="fil0"
                            points="0,9 59,68 0,126 9,135 68,77 126,135 135,126 77,68 135,9 126,0 68,59 9,0 "
                        /></g
                    >
                </svg>
            </button>
        </div>
        {#if new_event_form}
            <div in:slide out:fade class="flex flex-col mt-5">
                <div in:fade>
                    <div class="text-sm py-2">
                        1. Select the day of the week
                    </div>
                    <div
                        class="flex flex-row flex-wrap gap-4 text-sm mt-4 py-2"
                    >
                        {#each weekdays as weekday, index}
                            <div>
                                <input
                                    type="radio"
                                    class="hidden"
                                    id={index}
                                    name="weekday"
                                />
                                <label
                                    on:click={() => selectWeekDay(index)}
                                    for={index}
                                    class="bg-gray-100 text-center px-4 py-1 rounded-md text-black font-semibold cursor-pointer"
                                >
                                    {weekday}
                                </label>
                            </div>
                        {/each}
                    </div>
                </div>

                {#if new_event_weekday}
                    <div in:fade>
                        <div class="text-sm py-2 mt-4">
                            2. Select available time
                        </div>
                        <div
                            class="mt-2 flex flex-col py-2 px-4 gap-y-3 bg-white max-w-sm"
                        >
                            <Select
                                items={schedule_options}
                                on:select={handleScheduleSelect}
                                on:clear={handleScheduleClear}
                            />
                        </div>
                    </div>
                {/if}
                {#if new_event_timestamp_id}
                    <div in:fade>
                        <div class="text-sm py-2 mt-4">
                            3. Select setpoint for this thermostat {new_event_setpoint}
                            &deg;F
                        </div>
                        <div class="py-3">
                            <input
                                bind:value={new_event_setpoint}
                                type="range"
                                min="45"
                                max="90"
                                class="range range-sm range-primary"
                            />
                            <div
                                class="w-full flex justify-between text-xs px-2"
                            >
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                                <span>|</span>
                            </div>
                        </div>
                    </div>
                {:else if new_event_timestamp_id}
                    <div in:fade>
                        <div class="text-sm py-2 mt-4">3. Choose an action</div>
                        <div class="my-2 max-w-xs z-40 ml-4">
                            <Select
                                items={state_options}
                                placeholder="Which action to perform?"
                                placeholderAlwaysShow={true}
                                on:select={handleStateSelect}
                                on:clear={handleStateClear}
                            />
                        </div>
                    </div>
                {/if}
                <div class="flex flex-row gap-x-7 pt-5 items-center">
                    {#if new_event_timestamp_id}
                        <div>
                            <button
                                on:click={() => saveNewEvent()}
                                class="btn btn-primary btn-xs btn-wide"
                            >
                                Save
                            </button>
                        </div>
                    {/if}
                    <div>
                        <button
                            on:click|self={() => resetForm()}
                            class="btn btn-outline btn-xs"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </div>
    <div class="py-4 text-lg mt-4 font-semibold">Scheduled events</div>
    <div class="overflow-y-auto">
        {#each events as event}
            <div
                class="grid grid-cols-4 px-3 py-2 items-center text-sm max-w-screen-md shadow-md rounded-md"
            >
                <div>
                    {weekdays[event.schedule.week_day - 1]}
                </div>
                <div>
                    {event.schedule.checkpoint.substring(11, 16)}
                </div>
                <div>
                    {event.setpoint} °
                </div>
                <div>
                    <button
                        on:click={() => deleteEvent(event.id)}
                        class="btn btn-xs btn-warning"
                    >
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
    </div>
</div>

<style>
    input:checked + label {
        box-shadow: var(--tw-ring-inset) 0 0 0
            calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
    }

    #schedule-ui {
        z-index: 101;
    }
    #schedule-overlay {
        z-index: 100;
    }
</style>
