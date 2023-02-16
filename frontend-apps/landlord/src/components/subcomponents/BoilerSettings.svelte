<script>
// @ts-nocheck
import axios from 'axios';
import { getCsrfCookieValue } from '../../lib/utils';
import { message, messenger } from '../../stores/store';
import { createEventDispatcher } from 'svelte';
import RangeSlider from "svelte-range-slider-pips";
// import OffHoursSchedule from './OffHoursSchedule.svelte';
import Tooltip from '../shared/Tooltip.svelte';
// import { fade, scale } from 'svelte/transition';

export let boiler;

let vacant_setpoint = boiler.data.vacant_setpoint;
// let offhours_setpoint = boiler.data.offhours_setpoint;
let shutdown_temp = boiler.data.shutdown_temp;
// let offhours_enabled = boiler.data.offhours_enabled;
let shutdown_enabled = boiler.data.shutdown_enabled;

let vacant_apart_tooltip = false;
let wwsd_tooltip = false;

// let offhours_scheduling = false;

const vacant_apart_tooltip_content = 'Temperature value which is set on all thermostats in the apartment after its state changed to "vacant"';
// const offhours_tooltip_content = 'Temperature value which is set on thermostats during off-hours period of the day';
const wwsd_tooltip_contnent = 'Outdoor air temperature value which should trigger automatic boiler shutdown';

const dispatch = createEventDispatcher();

async function patchHeatingSettings(data) {

    const endpoint = `/api/devices/boiler/${boiler.data.id}/`;
    try {
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
            $message = "Heating settings were successfully updated"
            $messenger = true;
            dispatch('change');
        }
    } catch(error) {
            console.log(error)
    }
};

function handleVacantRangeChange(e) {
    const value = e.detail.values[0];
    vacant_setpoint = value;
    const data = {
        "vacant_setpoint": value,
    }
    patchHeatingSettings(data);
    dispatch('save');
};


function handleWWSDRangeChange(e) {
    const value = e.detail.values[0];
    shutdown_temp = value;
    const data = {
        "shutdown_temp": value,
    }
    patchHeatingSettings(data);
    dispatch('save');
};

function handleWWSDToggle() {
    shutdown_enabled = !shutdown_enabled;
    const data = {
        "shutdown_enabled": shutdown_enabled,
    }
    patchHeatingSettings(data);
    dispatch('save');
};
</script>



<div class="grid grid-cols-1 md:grid-cols-2 text-sm gap-y-4 gap-x-3 pt-3">
    <div class="flex flex-col gap-y-2 md:flex-row items-center gap-x-2">
        <div>Vacant t, °F </div>
        <div class="relative cursor-pointer" on:click={()=> vacant_apart_tooltip = !vacant_apart_tooltip}>
            <svg class="w-5 fill-current text-gray-500" viewBox="0 0 64 64" x="0px" y="0px"><g><path d="M36.984,43.682V45.6a.854.854,0,0,1-.854.854H27.87a.854.854,0,0,1-.854-.854V43.682a.854.854,0,0,1,.854-.854h1.721V30.113H28.247a.854.854,0,0,1-.8-1.154l.886-2.366a.855.855,0,0,1,.8-.554h4.421a.854.854,0,0,1,.854.854V42.828H36.13A.854.854,0,0,1,36.984,43.682ZM32,23.036a2.745,2.745,0,1,0-2.745-2.745A2.745,2.745,0,0,0,32,23.036ZM21.046,9.421a.994.994,0,0,0,.422-.093q.439-.205.886-.393a1,1,0,1,0-.773-1.844q-.485.2-.959.424a1,1,0,0,0,.424,1.906Zm-8.573,6.43a1,1,0,0,0,.751-.34,25.11,25.11,0,0,1,5.469-4.667,1,1,0,0,0-1.068-1.692,27.14,27.14,0,0,0-5.9,5.039,1,1,0,0,0,.751,1.66Zm30.059,38.82q-.439.206-.886.393a1,1,0,1,0,.773,1.844q.484-.2.959-.424a1,1,0,0,0-.846-1.813Zm8.244-6.183a25.11,25.11,0,0,1-5.469,4.667,1,1,0,0,0,1.068,1.692,27.14,27.14,0,0,0,5.9-5.039,1,1,0,0,0-1.5-1.32ZM32,55A23,23,0,1,1,55,32,23.026,23.026,0,0,1,32,55ZM53,32A21,21,0,1,0,32,53,21.024,21.024,0,0,0,53,32Z"></path></g></svg>
            {#if vacant_apart_tooltip}
                <Tooltip content={vacant_apart_tooltip_content} />
            {/if}
        </div>
    </div>
    <div class="slider-theme flex flex-col md:flex-row gap-2 items-center">
        <div class="flex-grow w-full md:w-11/12">
            <RangeSlider min={40} max={70} 
            values={[vacant_setpoint]} pips float 
            on:stop={(e) => handleVacantRangeChange(e)} />
        </div>
        <div class="w-24">
            <span class="font-semibold">{vacant_setpoint}</span> °F
        </div>
    </div>
    <div class="flex flex-col gap-y-2 md:flex-row items-center gap-x-2">
        <div> Warm weather automatic shutdown t, °F</div>
        <div class="relative cursor-pointer" on:click={()=> wwsd_tooltip = !wwsd_tooltip}>
            <svg class="w-5 fill-current text-gray-500 cursor-pointer" viewBox="0 0 64 64" x="0px" y="0px"><g><path d="M36.984,43.682V45.6a.854.854,0,0,1-.854.854H27.87a.854.854,0,0,1-.854-.854V43.682a.854.854,0,0,1,.854-.854h1.721V30.113H28.247a.854.854,0,0,1-.8-1.154l.886-2.366a.855.855,0,0,1,.8-.554h4.421a.854.854,0,0,1,.854.854V42.828H36.13A.854.854,0,0,1,36.984,43.682ZM32,23.036a2.745,2.745,0,1,0-2.745-2.745A2.745,2.745,0,0,0,32,23.036ZM21.046,9.421a.994.994,0,0,0,.422-.093q.439-.205.886-.393a1,1,0,1,0-.773-1.844q-.485.2-.959.424a1,1,0,0,0,.424,1.906Zm-8.573,6.43a1,1,0,0,0,.751-.34,25.11,25.11,0,0,1,5.469-4.667,1,1,0,0,0-1.068-1.692,27.14,27.14,0,0,0-5.9,5.039,1,1,0,0,0,.751,1.66Zm30.059,38.82q-.439.206-.886.393a1,1,0,1,0,.773,1.844q.484-.2.959-.424a1,1,0,0,0-.846-1.813Zm8.244-6.183a25.11,25.11,0,0,1-5.469,4.667,1,1,0,0,0,1.068,1.692,27.14,27.14,0,0,0,5.9-5.039,1,1,0,0,0-1.5-1.32ZM32,55A23,23,0,1,1,55,32,23.026,23.026,0,0,1,32,55ZM53,32A21,21,0,1,0,32,53,21.024,21.024,0,0,0,53,32Z"></path></g></svg>
        {#if wwsd_tooltip}
            <Tooltip content={wwsd_tooltip_contnent} />
        {/if}
        </div>
    </div>
    <div class="slider-theme flex flex-col md:flex-row gap-2 items-center">
        <div class="w-full md:w-10/12 flex-grow ">
            <RangeSlider min={40} max={70} 
            disabled={!shutdown_enabled}
            values={[shutdown_temp]} pips float on:stop={(e) => handleWWSDRangeChange(e)} />
        </div>
        <div class="flex flex-row items-center">
            <div class="w-12">
                <span class="font-semibold">{shutdown_temp}</span> °F
            </div>
            <div on:click={() => handleWWSDToggle()} class="w-8 cursor-pointer">
                <svg class="fill-current text-gray-400 transform transition-colors" class:text-green-500={shutdown_enabled===true}
                x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
                <title>{shutdown_enabled ? 'Enabled' : 'Disabled'} </title>
                <switch><g><path d="M50,2.5L50,2.5C23.8,2.5,2.5,23.8,2.5,50l0,0c0,26.2,21.3,47.5,47.5,47.5l0,0c26.2,0,47.5-21.3,47.5-47.5l0,0    C97.5,23.8,76.2,2.5,50,2.5z M45.7,24.2c0-2.4,1.9-4.3,4.3-4.3s4.3,1.9,4.3,4.3v21.6c0,2.4-1.9,4.3-4.3,4.3s-4.3-1.9-4.3-4.3V24.2    z M50,78.4c-15.2,0-27.6-12.4-27.6-27.6c0-8.7,4-16.7,11-22c1.9-1.4,4.6-1,6,0.8c1.4,1.9,1,4.6-0.8,6c-4.8,3.6-7.6,9.2-7.6,15.2    c0,10.5,8.5,19.1,19.1,19.1c10.5,0,19.1-8.5,19.1-19.1c0-6-2.8-11.5-7.6-15.2c-1.9-1.4-2.3-4.1-0.8-6c1.4-1.9,4.1-2.3,6-0.8    c7,5.3,11,13.3,11,22C77.6,66,65.2,78.4,50,78.4z"></path></g></switch></svg>      
            </div>
        </div>
    </div>
</div>
<!-- <div class="py-4 text-sm cursor-pointer" on:click={()=> offhours_scheduling = true}>
    Off-hours thermostat scheduling <span class="font-semibold">({ boiler.data.weekdays_offhours_enabled ||  boiler.data.weekend_offhours_enabled ? 'Active' : 'Disabled'}) </span> 
</div> 
{#if offhours_scheduling}
    <OffHoursSchedule boiler={boiler} on:close={() => offhours_scheduling = false} />
{/if} -->

<style>
    .slider-theme {
            --range-range: #458796;
            --range-handle: #458796;
            --range-handle-focus: #458796;
            --range-handle-inactive: #458796;
            /* --slider: rgba(59 130 246 ); */
        }
</style>