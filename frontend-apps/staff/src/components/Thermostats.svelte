<script>


import axios from 'axios';

import { onMount } from 'svelte';
import Controller from './subcomponents/Thermostat.svelte'
import { fade, slide } from 'svelte/transition';

let thermostats_list = new Array;

const endpoint = '/api/staff/smart-thermostats/';

onMount(() => {
    getThermostatData();
})

async function getThermostatData() {
    try {
    const response = await axios({
        url: endpoint,
        method: "get",

    });
    if(response.status === 200) {
            console.log("Controllers", response.data)
            thermostats_list = response.data;
        }
    } catch(error) {
            console.log(error)
    }
};

</script>

<div class="max-w-3xl" in:fade>
  <div class="text-xl font-semibold py-4">
    Smart thermostats list
  </div>
  <div class="grid grid-cols-2 font-semibold gap-4 p-6 border-b-2 pb-2">
    <div>
      S/n
    </div>
    <div>
      Status
    </div>
  </div>
  <div class="overflow-y-auto">
      {#each thermostats_list as thermostat}
      <div in:slide class="grid grid-cols-2 gap-4 p-6 text-sm shadow-md">
        <Controller thermostat={thermostat} />
      </div>
      {:else}
        Loading...
      {/each}
  </div>
</div>


<style>
</style>
  