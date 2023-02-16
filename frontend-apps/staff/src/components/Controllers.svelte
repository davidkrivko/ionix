<script>


import axios from 'axios';

import { onMount } from 'svelte';
import Controller from './subcomponents/Controller.svelte'
import { fade, slide } from 'svelte/transition';

let controllers_list = new Array;

const endpoint = '/api/staff/controllers/';

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
            controllers_list = response.data;
        }
    } catch(error) {
            console.log(error)
    }
};

</script>

<div class="max-w-3xl" in:fade>
  <div class="text-xl font-semibold py-4">
    Ioniq controllers list
  </div>
  <div class="grid grid-cols-4 font-semibold gap-4 p-6 border-b-2 pb-2 data-table">
    <div>
      S/n
    </div>
    <div class="hidden md:block">
      Owner
    </div>
    <div>
      Type
    </div>
    <div>
      Status
    </div>
  </div>
  <div class="overflow-y-auto">
      {#each controllers_list as controller}
      <div in:slide class="grid grid-cols-4 gap-4 p-6 text-sm data-table shadow-md">
        <Controller controller={controller} />
      </div>
      {:else}
        Loading...
      {/each}
  </div>
</div>


<style>
  .data-table {
    grid-template-columns: 1fr 1fr 1fr auto;
  }
</style>
  