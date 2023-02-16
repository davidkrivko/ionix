<script>
// @ts-nocheck

import { onMount } from 'svelte'; 
import axios from 'axios';
import { fade, slide } from 'svelte/transition';
import BoilerSettings from './subcomponents/BoilerSettings.svelte';
import HeatCyclesGraph from './subcomponents/HeatCyclesGraph.svelte';
import { getCsrfCookieValue, fetchIoniqOnlineStatus } from '../lib/utils';
// import ConfirmPopup from '../components/shared/ConfirmPopup.svelte';
import { message, messenger } from '../stores/store';

let apartments = [];
let boilers = {};
let address_filter = '';

let confirmation_popup = false;

onMount(()=>{
    getApartmentsWithBoilers();
})

async function getApartmentsWithBoilers(query = null) {
  
    let endpoint = `/api/users/owner/apartments/`;
    if (query !== null) endpoint += query;

    try {
    const response = await axios({
        url: endpoint,
        method: "get",

    });
    if(response.status === 200) {
            apartments = response.data;
            // console.log("apartments", apartments)
            boilers = mapBoilers(apartments);
            console.log("Boilers", boilers)
            // $wwsd_setpoint = boilers[0]['shutdown_temp'];
        }
    } catch(error) {
            console.log(error)
    }
};

function mapBoilers(apartments) {
    
    const boilers_set = new Set();
    const boilers_obj = new Object();

    apartments.forEach(x => {
        const id = x.boiler?.id;
        if (id === undefined) return undefined;

        if (!boilers_set.has(id)) {
            boilers_set.add(id);

            boilers_obj[id] = {
                'apartments': [x.name],
                'serial_num': x.boiler?.serial_num,
                'controller_serial_num': x.controller_sn,
                'address': x.building.address,
                'data': x.boiler,
            }
        } else {
            boilers_obj[id]['apartments'].push(x.name);
        }
    });
    return boilers_obj;

};

async function getEndSwitchStatus(value) {

  const endpoint = `/api/devices/boiler/iodata/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const boiler_id = value.data.id;
    const controller_sn = value.controller_serial_num;
    const data = {
      "id": boiler_id
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
            const res = response.data
            const endswitch = res.data?.endswitch;
            const systemp = res.data?.systemp;
            const online_status = await fetchIoniqOnlineStatus(controller_sn);
            return {
                'endswitch': endswitch,
                'systemp': systemp,
                'online_status': online_status,
            };
        }
    } catch(error) {
            console.log(error)
    }
};

function handleBuildingAddressFilter() {
    if (address_filter.length > 0) {
        const query_string = `?building=${address_filter}`
        getApartmentsWithBoilers(query_string);
    } else getApartmentsWithBoilers();
}


async function changeBoilerManualOverride(boiler_id, state) {

    const endpoint = `/api/devices/boiler/${boiler_id}/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
        "forced_endswitch_state": state
    }
    const response = await axios({
        url: endpoint,
        method: "patch",
        data: data,
        headers: {
            'X-CSRFToken': csrfcookie
        }

    });
    if(response.status === 200) {
            $message = "Boiler controll settings were successfully updated"
            $messenger = true;
            getApartmentsWithBoilers();
            // dispatch('change');
        }
    } catch(error) {
            console.log(error);
            $message = "Something went wrong. Please try again later";
            $messenger = true;
    }
};

let item_details = Array(Object.keys(boilers)).fill(null).map((x, index) => false);
</script>



<div class="flex flex-col h-full" in:fade>
    <div class="w-full gradient py-6 px-2 md:px-8 rounded-tr-2xl relative">
        <div class="text-xl md:text-3xl font-bold py-4 text-white tracking-wider pb-24">
            Boiler automation & settings
        </div>
        <div class="grid grid-cols-1 gap-x-5 gap-y-2 text-sm md:text-base md:absolute -bottom-8 left-8 font-medium">
            <!-- <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Building name</div>
                <div class="text-gray-600">
                    <input type="text" bind:value={name_filter} on:keyup={() => handleBuildingNameFilter()} 
                    placeholder="e.g. My first building"
                    class="py-2 px-2 bg-white box-border w-48 rounded-sm focus:outline-none">
                </div>
            </div> -->
            <div class="max-w-xs flex flex-col bg-opacity-30 text-sm md:text-md bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div class="py-2">Building adress</div>
                <div class="text-gray-600">
                    <input type="text" bind:value={address_filter} on:keyup={() => handleBuildingAddressFilter()} 
                    placeholder="e.g. 132 Parklane"
                    class="py-2 px-2 bg-white box-border w-full rounded-sm focus:outline-none">
                </div>
            </div>
        </div>
    </div>
    <div class="px-2 md:px-8 py-12 bg-gray-50 rounded-br-2xl flex flex-col flex-grow">
        <div
        class="md:boiler-grid-md grid grid-cols-2 md:grid-cols-4 font-semibold bg-white rounded-md mt-4 px-4 py-2 cursor-pointer gap-x-8 overflow-hidden text-sm md:text-md">
            <div class="px-2 text-sm md:text-md">
                Boilers
            </div>
            <div class="text-sm md:text-md">
                Status
            </div>
            <div class="text-sm md:text-md hidden md:block">
                Manual control
            </div>
            <div class="text-sm md:text-md hidden md:block">
                Apartments
            </div>
        </div>

        {#each Object.entries(boilers) as [key, value], index }
            <div on:click={() => item_details[index] = !item_details[index]}
            class="grid md:boiler-grid-md grid-cols-2 md:grid-cols-4 shadow-lg bg-white rounded-md mt-4 px-4 py-2 cursor-pointer gap-x-8 overflow-hidden text-sm md:text-md">
                <div class="px-2 flex flex-row gap-x-1">
                    <span>
                        <svg class="w-5 fill-current text-gray-500" version="1.0" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><polygon points="12.12994,59.5648422 13.2478781,59.5648422 13.2478781,41.7181549 10.3441458,41.7181549 "></polygon><polygon points="7.7453737,41.7181549 9.5293446,59.5648422 10.6324997,59.5648422 8.8542538,41.7181549 "></polygon><polygon points="5.6902847,41.7181549 5.6902847,59.5648422 8.0395775,59.5648422 6.2537827,41.7181549 "></polygon><path d="M81.5048218,41.1876793h-5.1128769V21.0179939H24.602951v20.1696854h-5.4933205v-2.1145325H14.506031v23.7536697h4.6035995  v-2.1156044h5.4933205V83.924469c0,2.3933868,1.9384022,4.3317947,4.3318539,4.3317947H72.059082  c2.3913803,0,4.3328629-1.9384079,4.3328629-4.3317947V60.7112122h5.1128769v2.1156044h4.6025925V39.0731468h-4.6025925V41.1876793z   M51.0308151,76.6295624c-3.1542168,0-5.7115974-2.5554276-5.7115974-5.7096481  c0-3.1553497,2.5573807-5.7148056,5.7115974-5.7148056c3.158371,0,5.7127953,2.5594559,5.7127953,5.7148056  C56.7436104,74.0741348,54.1891861,76.6295624,51.0308151,76.6295624z M51.0308151,61.2899361  c-6.3084373,0-11.4213753-5.1159592-11.4213753-11.4245224c0-6.3094444,5.1129379-11.4192963,11.4213753-11.4192963  c6.3096313,0,11.4225693,5.1098518,11.4225693,11.4192963C62.4533844,56.1739769,57.3404465,61.2899361,51.0308151,61.2899361z"></path><polygon points="92.7488022,42.3350601 94.5335312,60.1808014 95.0970306,60.1808014 95.0970306,42.3350601 "></polygon><polygon points="90.1549377,42.3350601 91.9340057,60.1808014 93.0418777,60.1808014 91.2590408,42.3350601 "></polygon><polygon points="87.5405045,42.3350601 87.5405045,60.1808014 90.4441071,60.1808014 88.6584396,42.3350601 "></polygon><path d="M76.3919449,16.3874702c0-2.3943319-1.9414825-4.3337402-4.3328629-4.3337402H28.9348049  c-2.3934517,0-4.3318539,1.9394083-4.3318539,4.3337402v3.0416203h51.7889938V16.3874702z"></path><circle cx="51.0315857" cy="70.9186249" r="2.9117377"></circle><path d="M51.0308151,41.9878273c-4.3519211,0-7.8806076,3.5296936-7.8806076,7.8775864  c0,4.3550034,3.5286865,7.8847618,7.8806076,7.8847618c4.3541222,0,7.8827477-3.5297585,7.8827477-7.8847618  C58.9135628,45.5175209,55.3849373,41.9878273,51.0308151,41.9878273z M51.0308151,51.4989815l-3.9977036-6.7373199  l5.8274689,5.1037521L51.0308151,51.4989815z"></path></svg>
                    </span>
                    <span>
                        {value.address} 
                    </span>
                </div>
                <div>
                {#if value.controller_serial_num}
                    {#await getEndSwitchStatus(value)}
                        ...
                        {:then value}

                        {#if value?.online_status === false}
                            <div in:fade title="Controller is offline">
                                <svg class="w-5 fill-current text-red-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g><path d="M50.048,61.368c4.418,0,8.421,1.798,11.323,4.699l4.691-4.691c-3.373-3.372-7.801-5.686-12.737-6.404l-6.799,6.8   C47.661,61.516,48.837,61.368,50.048,61.368z"></path><path d="M43.477,70.818l6.571,6.572l6.571-6.572c-1.681-1.683-4.006-2.723-6.571-2.722C47.482,68.097,45.158,69.136,43.477,70.818z   "></path><path d="M50.048,41.544c-9.882-0.001-18.845,4.02-25.336,10.51l4.693,4.691c3.758-3.757,8.535-6.491,13.872-7.764l7.421-7.422   C50.481,41.557,50.266,41.544,50.048,41.544z"></path><path d="M70.692,56.746l4.69-4.691c-3.255-3.255-7.133-5.888-11.435-7.705l-5.167,5.166C63.329,50.944,67.401,53.454,70.692,56.746   z"></path><path d="M50.048,28.319c-13.528,0-25.797,5.503-34.682,14.39l4.692,4.692c7.684-7.684,18.292-12.442,29.991-12.443   c2.286,0,4.527,0.187,6.717,0.537l5.605-5.606C58.432,28.865,54.303,28.319,50.048,28.319z"></path><path d="M68.905,39.392c4.137,2.062,7.897,4.771,11.134,8.006l4.69-4.691c-3.223-3.224-6.897-5.995-10.911-8.228L68.905,39.392z"></path></g><path d="M50.277,4.35C25.106,4.35,4.627,24.829,4.627,50c0,25.172,20.479,45.65,45.65,45.65c25.172,0,45.65-20.479,45.65-45.65  C95.928,24.829,75.449,4.35,50.277,4.35z M50.277,10.936c9.419,0,18.069,3.351,24.823,8.923L20.136,74.823  C14.564,68.069,11.213,59.419,11.213,50C11.213,28.46,28.738,10.936,50.277,10.936z M50.277,89.063  c-9.418,0-18.068-3.35-24.821-8.921L80.42,25.179c5.571,6.753,8.921,15.403,8.921,24.821C89.341,71.54,71.817,89.063,50.277,89.063z  "></path></svg>
                            </div>
                        {:else if value?.endswitch === 1}
                            <div title="Active">
                                <svg class="w-4 fill-current text-yellow-600"  viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                                    <g>
                                    <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                                    </path>
                                    </g>
                                </svg>
                            </div>
                        {:else}
                            <div title="Standby">
                                <svg class="w-4 fill-current text-gray-400"  viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                                    <g>
                                    <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                                    </path>
                                    </g>
                                </svg>
                            </div>
                        {/if}
                    {/await}
                {:else}
                    <div title="Boiler doesn't have controller connected or it is misconfigured">
                        <svg class="w-5 fill-current text-gray-400" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M50,5.5C25.424,5.5,5.5,25.424,5.5,50c0,24.577,19.924,44.5,44.5,44.5c24.577,0,44.5-19.923,44.5-44.5  C94.5,25.424,74.577,5.5,50,5.5z M50,16.5c6.971,0,13.442,2.131,18.804,5.774L22.274,68.805C18.631,63.443,16.5,56.971,16.5,50  C16.5,31.499,31.499,16.5,50,16.5z M50,83.5c-6.912,0-13.334-2.095-18.669-5.683l46.486-46.486C81.405,36.666,83.5,43.088,83.5,50  C83.5,68.501,68.501,83.5,50,83.5z"></path></svg>
                    </div>
                {/if}
                </div>
                <div class="md:flex flex-row gap-x-2 relative hidden flex-shrink-0">
                {#if value.controller_serial_num}
                <div class="w-12">
                    <button on:click|stopPropagation={() => changeBoilerManualOverride(value.data.id, 1)}
                        class:forced-active-orange={value.data.forced_endswitch_state === 1} 
                        class="py-0.5 ring-1 px-2 ring-gray-300 rounded-full text-gray-400 text-xs">
                        On
                    </button>
                </div>
                <div class="w-12">
                    <button on:click|stopPropagation={() => changeBoilerManualOverride(value.data.id, 0)}
                        class:forced-active-gray={value.data.forced_endswitch_state === 0} 
                        class="py-0.5 ring-1 px-2 ring-gray-300 rounded-full text-gray-400 text-xs">
                        Off
                    </button>
                </div>
                <div class="w-12">
                    <button on:click|stopPropagation={() => changeBoilerManualOverride(value.data.id, 2)}
                        class:forced-active-green={value.data.forced_endswitch_state === 2} 
                        class="py-0.5 ring-1 px-2 ring-gray-300 rounded-full text-gray-400 text-xs">
                        Auto
                    </button>
                </div>    
                {:else}
                <span>--</span>
                {/if}
                </div>
                <div class="hidden md:block overflow-x-auto">
                    {value.apartments.join(', ')} 
                </div>
            </div>
            <div class="mt-2 shadow-sm bg-white p-5" in:fade>
                <HeatCyclesGraph controller_sn={value.controller_serial_num} />
            </div>
            {#if item_details[index]}
                <div class="mt-2 shadow-sm bg-white p-5" in:fade>
                    <BoilerSettings boiler={value} />
                </div>
            {/if}
        {/each}
    </div>
</div>


<style>
    .gradient {
        background: #373B44;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #4286f4, #373B44);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #4286f4, #373B44); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    }
    .forced-active-green {
        background-color: rgb(24, 165, 118);
        color: #ffffff;
        font-weight: 600;
    }
    .forced-active-orange {
        background-color: #FEBE10;
        color: #ffffff;
        font-weight: 600;
    }
    .forced-active-gray {
        background-color: #5e5e5e;
        color: #ffffff;
        font-weight: 600;
    }
</style>