<script>
import axios from 'axios';
import { onMount } from 'svelte';
// import { getCsrfCookieValue } from '../lib/utils';
import { fade } from 'svelte/transition';
import {
    wwsd_setpoint,
} from '../stores/store';

import OutdoorTemp from './shared/OutdoorTemp.svelte';
import Troubleshooting from './subcomponents/Troubleshooting.svelte';
import WarmWeatherSettings from './subcomponents/WarmWeatherSettings.svelte';

let boilers = [];
let troubleshooting_block = false;

onMount(() => {
    // console.log("thermostat", thermostat)
    getBoilers();

})

async function getBoilers() {
  
  const endpoint = `/api/devices/boiler/all/`;
    try {
    const response = await axios({
        url: endpoint,
        method: "get",

    });
    if(response.status === 200) {
            boilers = response.data;
            $wwsd_setpoint = boilers[0]['shutdown_temp'];
        }
    } catch(error) {
            console.log(error)
    }
};


</script>

<div in:fade >
    <OutdoorTemp />

    <div class="mx-auto max-w-lg">
        <div class="text-lg font-semibold mt-10 py-4">
            BOILER SETTINGS
        </div>
        <div class="py-2 text-sm">Set outdoor temperature value for boiler automatic shutdown</div>

        {#each boilers as boiler, index }
            <WarmWeatherSettings {boiler} on:reload={() => getBoilers()}/>
            
        {/each}
        <div class="flex flex-row items-center gap-x-5 mt-4 py-4">
            <div>
                <h2 class="font-semibold">
                    Troubleshooting information
                </h2>    
            </div>
            <div >
                <button on:click={() => troubleshooting_block = !troubleshooting_block}
                    class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">
                    {#if !troubleshooting_block}
                        Load
                    {:else}
                        Hide
                    {/if}
                </button>
            </div>
        </div>
        {#if troubleshooting_block}
            <Troubleshooting />
        {/if}
    </div>
</div>