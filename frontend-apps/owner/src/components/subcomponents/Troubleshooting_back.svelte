<script>
import axios from "axios";
import { onMount } from 'svelte';
import { slide } from 'svelte/transition';
import { wwsd_setpoint, outdoor_temp } from '../../stores/store';

onMount(() => {
    const fetch_interval = setInterval(()=> fetchData(), 1000);
    // fetchData();
    return () => clearInterval(fetch_interval);
})

let fetched_objects = [];

async function fetchData() {
    try {
    const endpoint = `/api/devices/controller/data/`;
  
    const response = await axios({
        url: endpoint,
        method: "get",
     });
    if(response.status === 200) {
        fetched_objects = response.data;
        }
    } catch(error) {
            console.log(error)
    }
};
</script>


<div class="max-w-md py-6">
        <div in:slide>
            <div class="grid grid-cols-2 gap-2 text-sm py-2 px-4 rounded-md shadow-md">
                <div>
                    Outdoor:
                </div>
                <div>
                    {$outdoor_temp || '--'} °
                </div>
                <div>
                    Warm Weather Shutdown Setpoint:
                </div>
                <div>
                    {$wwsd_setpoint || '--'} °
                </div>
            </div>

            {#each fetched_objects as obj}
            <div in:slide>
                <div class="font-semibold mt-4">
                   # {obj.data.controller.sn}
                </div>

                {#if obj.data.model_type === 'MX'}
                <div in:slide class="grid grid-cols-2 gap-2 text-sm py-2 px-4 rounded-md shadow-md">
                    <div>
                        Boiler:
                    </div>
                    <div>
                        {obj.data.controller.endswitch === 1 ? 'ON' : 'OFF'}
                    </div>
                    <div>
                        Boiler Current:
                    </div>
                    <div>
                        {obj.data.controller.icsboiler} A
                    </div>
                    <div>
                        System Current:
                    </div>
                    <div>
                        {obj.data.controller.icsmain} A
                    </div>
                    <div>
                        System Pressure:
                    </div>
                    <div>
                        {obj.data.controller.ps} PSI
                    </div>
                </div>
                <div in:slide class="rounded-md shadow-md mt-4 px-4">
                    <div class="pt-4 pb-2 font-semibold">
                        Pumps
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-sm py-2">
                        {#if obj.data.zones.icsz1 !== null}
                        <div>
                            {obj.data.zones.icsz1 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.icsz1} A
                        </div>
                        {/if}
                        {#if obj.data.zones.icsz2 !== null}
                        <div>
                            {obj.data.zones.icsz2 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.icsz2} A
                        </div>
                        {/if}
                        {#if obj.data.zones.icsz3 !== null}
                        <div>
                            {obj.data.zones.icsz3 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.icsz3} A
                        </div>
                        {/if}
                    </div>
                </div>
                <div in:slide class="rounded-md shadow-md mt-4 px-4">
                    <div class="pt-4 pb-2 font-semibold">
                        Temperature Sensors
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-sm py-2">
                        {#if obj.data.zones.t1 !== null}
                        <div>
                            {obj.data.zones.t1 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t1} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t2 !== null}
                        <div>
                            {obj.data.zones.t2 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t2} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t3 !== null}
                        <div>
                            {obj.data.zones.t3 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t3} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t4 !== null}
                        <div>
                            {obj.data.zones.t4 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t4} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t5 !== null}
                        <div>
                            {obj.data.zones.t5 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t5} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t6 !== null}
                        <div>
                            {obj.data.zones.t6 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t6} °
                        </div>
                        {/if}
                        {#if obj.data.zones.t7 !== null}
                        <div>
                            {obj.data.zones.t7 || 'Not defined'}:
                        </div>
                        <div>
                            {obj.data.controller.t7} °
                        </div>
                        {/if}
                    </div>
                </div>
                {:else if obj.data.model_type === "MN"}
                <div in:slide class="grid grid-cols-2 gap-2 text-sm py-2 px-4 rounded-md shadow-md mt-4">
                    <div>
                        Boiler endswitch:
                    </div>
                    <div>
                        {obj.data.controller.endswitch === 1 ? 'ON' : 'OFF'}
                    </div>
                    <div>
                        System temperature:
                    </div>
                    <div>
                        {obj.data.controller.systemp} °
                    </div>
                </div>
                {:else}
                        <div class="p-6 text-sm">
                            Fetching data...
                        </div>
                {/if}
            </div>      
            {/each}
        </div>
</div>