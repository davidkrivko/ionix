<script>
import axios from "axios";
import { onMount } from 'svelte';
import { scale, slide } from 'svelte/transition';
import { createEventDispatcher } from "svelte";
import { message, messenger } from '../../stores/store';

// import { wwsd_setpoint, outdoor_temp } from '../../stores/store';

export let boiler_id;


let error_message = '';

onMount(() => {
    // const fetch_interval = setInterval(()=> fetchData(), 1000);
    if (boiler_id !== undefined) {
    fetchData();

    }
    // return () => clearInterval(fetch_interval);
})

let master_controller;
let slave_controller;

const dispatch = createEventDispatcher();

async function fetchData() {
    try {
    const endpoint = `/api/devices/boiler/troubleshoot/${boiler_id}/`;
  
    const response = await axios({
        url: endpoint,
        method: "get",
     });
    if(response.status === 200) {
            groupControllerData(response.data)
            // if (response.data?.length === 0) {
            //     error_message = "No device data available"
            // }
        }
    } catch(error) {
            console.log(error)
            error_message = "No device data available"
    }
};

function groupControllerData(objects) {
    // Filter controllers 
    for (const obj of objects) {
        const controller_data = obj.data
        if (controller_data.is_master === true) {
            master_controller = controller_data;
        } else {
            slave_controller = controller_data;
        }
    }
    
};

</script>


<div on:click|self={() => dispatch('close')}
class="absolute flex flex-col justify-center items-center w-full h-full top-0 left-0 bg-black bg-opacity-40 cursor-pointer z-50">
    <div in:scale class="bg-white max-w-md p-5 rounded-md relative">
        <div class="absolute top-1 right-1">
            <button on:click={()=> dispatch('close')}>
                <svg class="w-8 text-gray-700 fill-current" viewBox="0 0 48 48" x="0px" y="0px"><g data-name="Application, Close"><path d="M25.41,24l11.3,11.29-1.42,1.42L24,25.41,12.71,36.71l-1.42-1.42L22.59,24,11.29,12.71l1.42-1.42L24,22.59l11.29-11.3,1.42,1.42Z"></path></g></svg>
            </button>
        </div>
        <div in:slide class="mt-4">
        {error_message}

        {#if master_controller}
            <!-- <div class="font-semibold mt-4">
                # {master_controller.controller.sn}
            </div> -->

            {#if master_controller.model_type === 'MX'}
            <div in:slide class="grid grid-cols-2 gap-4 text-sm py-2 px-4 rounded-md shadow-md bg-white">
                <div>
                    Boiler:
                </div>
                <div>
                    {master_controller.controller.endswitch === 1 ? 'ON' : 'OFF'}
                </div>
                <div>
                    Boiler Current:
                </div>
                <div>
                    {master_controller.controller.icsboiler} A
                </div>
                <div>
                    System Pressure:
                </div>
                <div>
                    {master_controller.controller.ps} PSI
                </div>
                <div>
                    System temperature:
                </div>
                <div>
                    {master_controller.system_temp}  °F
                </div>
            </div>
            <div in:slide class="rounded-md shadow-md mt-4 px-4 bg-white">
                <div class="pt-4 pb-2 font-semibold">
                    Pumps
                </div>
                <div class="grid grid-cols-2 gap-2 text-sm py-2">
                    {#if master_controller.zone_currents.icsz1 !== null}
                    <div>
                        {master_controller.zone_currents.icsz1}:
                    </div>
                    <div>
                        {master_controller.controller.icsz1} A
                    </div>
                    {/if}
                    {#if master_controller.zone_currents.icsz2 !== null}
                    <div>
                        {master_controller.zone_currents.icsz2}:
                    </div>
                    <div>
                        {master_controller.controller.icsz2} A
                    </div>
                    {/if}
                    {#if master_controller.zone_currents.icsz3 !== null}
                    <div>
                        {master_controller.zone_currents.icsz3}:
                    </div>
                    <div>
                        {master_controller.controller.icsz3} A
                    </div>
                    {/if}

                    {#if slave_controller}
                        {#if slave_controller.zone_currents.icsz1 !== null}
                        <div>
                            {slave_controller.zone_currents.icsz1}:
                        </div>
                        <div>
                            {slave_controller.controller.icsz1} A
                        </div>
                        {/if}
                        {#if slave_controller.zone_currents.icsz2 !== null}
                        <div>
                            {slave_controller.zone_currents.icsz2}:
                        </div>
                        <div>
                            {slave_controller.controller.icsz2} A
                        </div>
                        {/if}
                        {#if slave_controller.zone_currents.icsz3 !== null}
                        <div>
                            {slave_controller.zone_currents.icsz3}:
                        </div>
                        <div>
                            {slave_controller.controller.icsz3} A
                        </div>
                        {/if}

                    {/if}
                </div>
            </div>
            <div in:slide class="rounded-md shadow-md mt-4 px-4 bg-white">
                <div class="pt-4 pb-2 font-semibold">
                    Temperature Sensors
                </div>
                <div class="grid grid-cols-2 gap-2 text-sm py-2">
                    {#each master_controller.pipe_temps as zone }
                        <div>
                            {zone.name}:
                        </div>
                        <div  class="flex flex-wrap">
                            Supply: {zone['SPL'] || 'n/a'} °F <br/> Return: {zone['RTN'] || 'n/a'} °F
                        </div>
                    {/each}

                    {#if slave_controller}
                        {#each slave_controller.pipe_temps as zone }
                        <div>
                            {zone.name}:
                        </div>
                        <div class="flex flex-wrap">
                            Supply: {zone['SPL'] || 'n/a'} °F <br/> Return: {zone['RTN'] || 'n/a'}  °F
                        </div>
                        {/each}
                    {/if}
                </div>
            </div>
            {:else if master_controller.model_type === "MN"}
            <div in:slide class="grid grid-cols-2 gap-4 text-sm py-2 px-4 rounded-md shadow-md mt-4 bg-white">
                <div>
                    Boiler endswitch:
                </div>
                <div>
                    {master_controller.controller.endswitch === 1 ? 'ON' : 'OFF'}
                </div>
                <div>
                    System temperature:
                </div>
                <div>
                    {master_controller.controller.systemp} °
                </div>
            </div>
            {:else}
                <div class="p-6 text-sm">
                    Fetching data...
                </div>
            {/if}
        {/if}
        </div>
        
    </div>
</div>