<script>
// @ts-nocheck

import { onMount } from 'svelte'; 
import axios from 'axios';
import { getCsrfCookieValue } from '../../lib/utils';
import { fade, slide } from 'svelte/transition';
import { message, messenger } from '../../stores/store';
import { createEventDispatcher } from 'svelte';
import RangeSlider from "svelte-range-slider-pips";
import ThermostatStatus from '../shared/ThermostatStatus.svelte';

export let apartment;
export let temp_range;

onMount(()=>{
    loadRooms();
})

let rooms = [];
let thermostat_limits_block = false;
let min_temp = temp_range[0];
let max_temp = temp_range[1];
let tlimits_is_on = apartment.tlimits_is_on;

const dispatch = createEventDispatcher();

async function loadRooms() {
  try {
  const endpoint = `/api/users/owner/apartment/${apartment.id}/`;
  const response = await axios({
      url: endpoint,
      method: "get",

  });
  if(response.status === 200) {
        const res = response.data;
        console.log("Rooms", res)
        rooms = res;
      }
  } catch(error) {
        console.log(error)
  }
};


async function updateThermostatLimits() {
  
  const endpoint = `/api/users/owner/apartment/limits/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "id": apartment.id,
      "min_temp": min_temp,
      "max_temp": max_temp,
      "tlimits_is_on": tlimits_is_on,
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
            // console.log(response.data.data)
            $message = response.data.detail;
            $messenger = true;
            // thermostat_limits_block = false;
            dispatch('change');
        }
    } catch(error) {
            console.log(error)
    }
};

function handleRangeSelect(e) {
    const range = e.detail.values;
    min_temp = range[0];
    max_temp = range[1];
    updateThermostatLimits();
}

function toggleThermostatLimitation() {
    tlimits_is_on = !tlimits_is_on;
    updateThermostatLimits();
}
</script>



{#each rooms as room }
<div in:slide class="">
        {#if room.thermostat}
            <ThermostatStatus room={room} />
        {/if}
</div>
{/each}

<div class="mt-4">
    <button on:click={() => thermostat_limits_block = !thermostat_limits_block}
        class="flex flex-row items-center gap-x-4 py-1.5 px-6 cursor-pointer shadow-sm text-sm bg-gray-100 text-gray-600 rounded-sm active:shadow-md">
             <span>
                Temp. range {min_temp || '--'} — {max_temp || '--'} °F {tlimits_is_on ? '(Activated)' : '(Disabled)'}
            </span>
            <span>        
                <svg class="w-4 fill-current text-gray-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><switch><foreignObject requiredExtensions="http://ns.adobe.com/AdobeIllustrator/10.0/" x="0" y="0" width="1" height="1"></foreignObject><g i:extraneous="self"><g><path d="M5273.1,2400.1v-2c0-2.8-5-4-9.7-4s-9.7,1.3-9.7,4v2c0,1.8,0.7,3.6,2,4.9l5,4.9c0.3,0.3,0.4,0.6,0.4,1v6.4     c0,0.4,0.2,0.7,0.6,0.8l2.9,0.9c0.5,0.1,1-0.2,1-0.8v-7.2c0-0.4,0.2-0.7,0.4-1l5.1-5C5272.4,2403.7,5273.1,2401.9,5273.1,2400.1z      M5263.4,2400c-4.8,0-7.4-1.3-7.5-1.8v0c0.1-0.5,2.7-1.8,7.5-1.8c4.8,0,7.3,1.3,7.5,1.8C5270.7,2398.7,5268.2,2400,5263.4,2400z"></path><path d="M5268.4,2410.3c-0.6,0-1,0.4-1,1c0,0.6,0.4,1,1,1h4.3c0.6,0,1-0.4,1-1c0-0.6-0.4-1-1-1H5268.4z"></path><path d="M5272.7,2413.7h-4.3c-0.6,0-1,0.4-1,1c0,0.6,0.4,1,1,1h4.3c0.6,0,1-0.4,1-1C5273.7,2414.1,5273.3,2413.7,5272.7,2413.7z"></path><path d="M5272.7,2417h-4.3c-0.6,0-1,0.4-1,1c0,0.6,0.4,1,1,1h4.3c0.6,0,1-0.4,1-1C5273.7,2417.5,5273.3,2417,5272.7,2417z"></path></g><g><path d="M55.5,19.2c-23.2,0-42,18.9-42,42c0,11.2,4.4,21.8,12.3,29.7c1,1,2.8,1,3.9,0l6.9-6.9c1.1-1.1,1.1-2.8,0-3.9     c-1.1-1.1-2.8-1.1-3.9,0l-4.9,4.9c-5.1-5.9-8.1-13.3-8.7-21.1h6.9c1.5,0,2.7-1.2,2.7-2.7s-1.2-2.7-2.7-2.7h-6.9     c0.6-8,3.8-15.3,8.7-21.1l4.8,4.8c0.5,0.5,1.2,0.8,1.9,0.8c0.7,0,1.4-0.3,1.9-0.8c1.1-1.1,1.1-2.8,0-3.9l-4.8-4.8     c5.7-5,13-8.1,21.1-8.7v6.9c0,1.5,1.2,2.7,2.7,2.7s2.7-1.2,2.7-2.7v-6.9c8,0.6,15.3,3.8,21.1,8.7l-4.9,4.9     c-1.1,1.1-1.1,2.8,0,3.9c0.5,0.5,1.2,0.8,1.9,0.8s1.4-0.3,1.9-0.8l4.9-4.9c5,5.7,8.1,13,8.7,21.1H85c-1.5,0-2.7,1.2-2.7,2.7     S83.5,64,85,64h6.9c-0.6,7.8-3.6,15.1-8.7,21.1l-4.9-4.9c-1.1-1.1-2.8-1.1-3.9,0c-1.1,1.1-1.1,2.8,0,3.9l6.9,6.9     c0.5,0.5,1.2,0.8,1.9,0.8c0,0,0,0,0,0c0.7,0,1.4-0.3,1.9-0.8c7.9-8,12.3-18.5,12.3-29.7C97.5,38.1,78.6,19.2,55.5,19.2z"></path><path d="M55.5,52.7c-1.3,0-2.6,0.3-3.7,0.9L44,45.9c-1.1-1.1-2.8-1.1-3.9,0c-1.1,1.1-1.1,2.8,0,3.9l7.8,7.8     c-0.6,1.1-0.9,2.4-0.9,3.7c0,4.7,3.8,8.5,8.5,8.5s8.5-3.8,8.5-8.5S60.2,52.7,55.5,52.7z M55.5,64.3c-1.7,0-3-1.4-3-3     c0-1.7,1.4-3,3-3c1.7,0,3,1.4,3,3C58.5,62.9,57.1,64.3,55.5,64.3z"></path><path d="M22.4,25.4v-10c0-1.5-1.2-2.7-2.7-2.7c-1.5,0-2.7,1.2-2.7,2.7v3.4L7.2,9.1C6.1,8,4.4,8,3.3,9.1s-1.1,2.8,0,3.9l9.7,9.7     H9.6c-1.5,0-2.7,1.2-2.7,2.7c0,1.5,1.2,2.7,2.7,2.7h10C21.2,28.1,22.4,26.9,22.4,25.4z"></path></g></g></switch></svg>
            </span>
    </button>
</div>


{#if thermostat_limits_block}
<div transition:slide  class="py-4 max-w-xs relative">
    <div class="text-sm text-gray-600 py-2">
        Temperature limits for this appartment
    </div>
    <div class="slider-theme py-4">
        <RangeSlider min={40} max={70} values={[min_temp, max_temp]} disabled={!tlimits_is_on} on:stop={(e) => handleRangeSelect(e)}  range pips float />
    </div>
    <div class="mt-4 ml-2">
        <button on:click={() => toggleThermostatLimitation()}
            class:ring-2={tlimits_is_on}
            title={tlimits_is_on ? 'Activated' : 'Disabled'}
            class="bg-gradient-to-b from-gray-300 to-gray-50 shadow-sm px-4 py-2 text-sm flex flex-row items-center gap-x-3 ring-info-light">
                <span class="text-gray-800">
                   {#if tlimits_is_on}
                        Active
                    {:else}
                        Disabled
                    {/if}
                </span>
                <span>
                    <svg class="w-4 fill-current text-white" class:text-info-light={tlimits_is_on} viewBox="0 0 512 512" x="0px" y="0px"><path d="M347,50.84c-0.12,2.21-.34,4.29-0.34,6.38,0,22.67.13,45.35-.13,68-0.06,4.88,1.83,7.48,5.63,10.27,52.62,38.68,77.38,90.49,70.4,155.75-10.08,94.23-98.35,161.33-191.76,146.81-67.86-10.55-123.09-61.42-138.39-127.45-15.68-67.72,10.29-135.4,67.45-175.26,3.47-2.42,5-4.78,5-9.1-0.21-23.38-.09-46.76-0.12-70.15,0-1.74-.3-3.49-0.47-5.39C69.65,87.88-2.58,195.33,20,317.21,41.41,433.1,148.32,517.77,268.36,511.69c121.49-6.15,219.15-102.62,227.28-224C503.3,173.37,428.77,81.11,347,50.84Z"></path><path d="M293,0H219V281h74V0Z"></path></svg>
                </span>
        </button>
    </div>
</div>
{/if}


<style>
    .slider-theme {
        --range-range: #458796;
        --range-handle: #458796;
        --range-handle-focus: #458796;
        --range-handle-inactive: #458796;
    }
</style>