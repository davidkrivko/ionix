<script>
import axios from 'axios';
import { getCsrfCookieValue } from '../../lib/utils';
import RangeSlider from "svelte-range-slider-pips";
import { onMount } from 'svelte';
import {
    message,
    messenger,
} from '../../stores/store';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let boiler;

let shutdown_temp, shutdown_enabled;


onMount(() => {
    console.log("Boiler", boiler)
    shutdown_temp = boiler.shutdown_temp;
    shutdown_enabled = boiler.shutdown_enabled;
})

async function saveSetPointTemp(
    boiler_id, 
    shutdown_temp, 
    shutdown_enabled,
    ) {
    console.log("Posting new setpoint")
    try {
    const endpoint = '/api/devices/boiler/setshuttemp/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "boiler_id": boiler_id,
      "shutdown_temp": shutdown_temp,
      "shutdown_enabled": shutdown_enabled,
    }
    const response = await axios({
        url: endpoint,
        method: "post",
        data: data,
        headers: {
          'X-CSRFToken': csrfcookie
        }

    });
    if(response.status === 200) {
            $message = response.data.detail;
            $messenger = true;
        }
    } catch(error) {
            console.log(error)
            $message =  "Something went wrong 🤖. Please, try again later."
            $messenger = true;
    }
};

function saveData() {
    saveSetPointTemp(boiler.id, shutdown_temp, shutdown_enabled);
    dispatch('reload');
}

</script>

            
<div class="mt-4 bg-white px-5 py-4 shadow-md rounded-md">

    <div class="flex flex-row mt-2 gap-x-2 flex-wrap items-center">
        <div class="w-10/12">
            <RangeSlider values={[shutdown_temp]} pips min={35} max={70} step={1} float all='label' pipstep={5}
            on:stop={(e) => {shutdown_temp = e.detail.value; saveData()}} force_float={true}
        />
        </div>
        <div class="flex flex-col justify-start cursor-pointer" on:click={()=> {shutdown_enabled = !shutdown_enabled; saveData()}}>
            <div>
            <svg class="w-8 fill-current text-gray-400 transform transition-colors" class:text-green-400={shutdown_enabled === true}
            x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
            <title>Status: {shutdown_enabled ? 'On' : 'Off'}</title>
            <switch><g><path d="M50,2.5L50,2.5C23.8,2.5,2.5,23.8,2.5,50l0,0c0,26.2,21.3,47.5,47.5,47.5l0,0c26.2,0,47.5-21.3,47.5-47.5l0,0    C97.5,23.8,76.2,2.5,50,2.5z M45.7,24.2c0-2.4,1.9-4.3,4.3-4.3s4.3,1.9,4.3,4.3v21.6c0,2.4-1.9,4.3-4.3,4.3s-4.3-1.9-4.3-4.3V24.2    z M50,78.4c-15.2,0-27.6-12.4-27.6-27.6c0-8.7,4-16.7,11-22c1.9-1.4,4.6-1,6,0.8c1.4,1.9,1,4.6-0.8,6c-4.8,3.6-7.6,9.2-7.6,15.2    c0,10.5,8.5,19.1,19.1,19.1c10.5,0,19.1-8.5,19.1-19.1c0-6-2.8-11.5-7.6-15.2c-1.9-1.4-2.3-4.1-0.8-6c1.4-1.9,4.1-2.3,6-0.8    c7,5.3,11,13.3,11,22C77.6,66,65.2,78.4,50,78.4z"></path></g></switch></svg>
            </div>
        </div>
    </div>

<!-- <div class="flex flex-row py-4 pl-4">
    <span>Setpoint:</span> 
    <span class="ml-1 font-semibold">{boiler.shutdown_temp || '35' } °F</span>
</div> -->

</div>