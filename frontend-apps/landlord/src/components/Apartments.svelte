<script>
import { onMount } from 'svelte'; 
import axios from 'axios';
import { fade, slide } from 'svelte/transition';
import { message, messenger, selected_building, selected_dashboard_component } from '../stores/store';
import { getCsrfCookieValue, fetchIoniqOnlineStatus } from '../lib/utils';
import Rooms from './subcomponents/Rooms.svelte';
import Troubleshooting from './subcomponents/Troubleshooting.svelte';
import Tenants from './subcomponents/Tenants.svelte';
import Select from 'svelte-select';
import ConfirmPopup from './shared/ConfirmPopup.svelte';

let apartments = [];

let occupancy_options = [ 
    {value: '', label: 'Show all'},
    {value: 'false', label: 'Occupied only'},
    {value: 'true', label: 'Vacant only'},
]

let alert_options = [ 
    {value: '', label: 'Show all'},
    {value: 'true', label: 'With Alert status'},
    // {value: 'false', label: 'Without Alert status'},
]

let leaseholder_filter='';
let is_alert = '';
let is_vacant = '';
let outdoor_temp;

onMount(()=>{
    loadApartments();
    getZipTemperature();
})

async function loadApartments() {
  try {
  const endpoint = `/api/users/owner/apartments/?build_id=${$selected_building.id}&leaseholder=${leaseholder_filter}&is_alert=${is_alert}&is_vacant=${is_vacant}`;
  const response = await axios({
      url: endpoint,
      method: "get",

  });
  if(response.status === 200) {
        apartments = response.data;
        console.log("apartments", apartments)
      }

  } catch(error) {
        console.log(error)
  }
};

async function getEndSwitchStatus(apartment) {
// Fetches endswitch value and controller's 
// online status update
  
  const endpoint = `/api/devices/boiler/iodata/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const boiler_id = apartment.boiler.id;
    const controller_sn = apartment.controller_sn;

    const data = {
      "id": boiler_id,
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
        console.log("resp", response.data)
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

async function makeApartmentVacant(apartment_id, index) {
  
  const endpoint = `/api/users/owner/apartment/vacant/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "id": apartment_id,
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
            $message = "Appartment status was changed to 'Vacant'"
            $messenger = true;
            vacant_popup_items[index] = false;
            loadApartments();
        }
    } catch(error) {
            console.log(error)
    }
};

async function getZipTemperature() {
    try {
    const endpoint = `/api/properties/gettemp/?build_id=${$selected_building.id}`;
  
    const response = await axios({
        url: endpoint,
        method: "get",
     });
    if(response.status === 200) {
        const res = response.data;
        outdoor_temp = res.data.temp_f;
        }
    } catch(error) {
        console.log(error)
    }
};




function handleOccupancySelect(e) {
    is_vacant = e.detail.value;
    loadApartments();
};

function handleOccupancyClear() {
    is_vacant='';
    loadApartments();
};

function handleAlertSelect(e) {
    is_alert = e.detail.value;
    loadApartments();
};
function handleAlertClear() {
    is_alert = '';
    loadApartments();
}

function handleLeaseholderFilter() {
    loadApartments();
};

// let selection_list = [];
let item_details = Array(apartments).fill(null).map((x, index) => false);
let item_tenants = Array(apartments).fill(null).map((x, index) => false);
let vacant_popup_items= Array(apartments).fill(null).map((x, index) => false);
let troubleshooting_blocks = Array(apartments).fill(null).map((x, index) => false);

function toggleDropdownView(index) {
    item_details[index] = !item_details[index];
    item_tenants[index] = !item_tenants[index];
}
function toggleRawDropdown(index) {
    if (item_tenants[index]) {
        item_tenants[index] = false;
        item_details[index] = false;
    } else item_details[index] = !item_details[index];
}
</script>



<div class="flex flex-col h-full" in:fade>
    <div class="w-full gradient py-6 px-2 md:px-8 rounded-tr-2xl relative">
        <div class="flex flex-col md:flex-row">
            <div>
                <div class="flex flex-row items-center text-xl md:text-3xl gap-x-4 font-bold py-4 text-white tracking-wider">
                    <span>
                        <svg class="w-10 fill-current text-gray-50" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><switch><foreignObject requiredExtensions="http://ns.adobe.com/AdobeIllustrator/10.0/" x="0" y="0" width="1" height="1"></foreignObject><g i:extraneous="self"><path d="M11.1,60.1l10.2-2.6v4.5L11.1,64V60.1z M11.1,56.2L21.3,53v-4.5l-10.2,3.9V56.2z M24.3,93l16.6,4.4v-10l-16.6-2.2V93z     M11.1,71.7l10.2-0.6v-4.5l-10.2,1.2V71.7z M11.1,33l10.2-7.2v-4.5l-10.2,7.8V33z M11.1,25.2l10.2-8.5v-7l-10.2,9.8V25.2z     M11.1,48.5l10.2-4.5v-4.5l-10.2,5.2V48.5z M11.1,40.7l10.2-5.9v-4.5l-10.2,6.5V40.7z M11.1,79.5l10.2,0.7v-4.5l-10.2-0.1V79.5z     M61,26.6l-17.3-8.9v5.8l17.3,8L61,26.6z M24.3,8.7v5.6l4.1-3.4L24.3,8.7z M61,13.6L43.8,2.1v9.7L61,21.5L61,13.6z M61,46.2    l-17.3-5.3v5.8L61,51.1L61,46.2z M61,36.5l-17.3-7.2v5.8L61,41.2L61,36.5z M61.1,75.8H43.8v5.8l17.3-1.1V75.8z M61,56.1l-17.3-3.5    v5.8L61,61L61,56.1z M61,65.9l-17.3-1.7v5.9l17.3,0.8L61,65.9z M11.1,89.7l10.2,2.6v-7.5l-10.2-1.4V89.7z M24.3,33.2l16.6-9.5    v-5.8L24.3,28.5V33.2z M24.3,42.6l16.6-7.4v-5.8l-16.6,8.4V42.6z M24.3,23.7l16.6-11.7V2.5L24.3,16.2V23.7z M43.8,87.5v10.1    l17.3-3.6l0-8.3L43.8,87.5z M24.3,71l16.6-1v-5.8l-16.6,2V71z M24.3,80.4l16.6,1.2v-5.8l-16.6-0.1V80.4z M24.3,52.1l16.6-5.2V41    l-16.6,6.3V52.1z M24.3,61.5l16.6-3.1v-5.8l-16.6,4.2V61.5z M75.5,46.5l13.8,4.9l0-3.4l-13.8-5.7V46.5z M75.5,54.8l13.8,3.5l0-3.4    l-13.8-4.2V54.8z M75.5,38.1l13.8,6.4l0-3.4L75.5,34V38.1z M75.5,23.2v6.7l13.8,7.7l0-5L75.5,23.2z M75.5,63.1l13.8,2.1l0-3.4    l-13.8-2.8V63.1z M75.5,90.8l13.8-3l0-5.3l-13.8,1.5V90.8z M63.9,89.7l8.7,1.3V23l-8.7,4.9V89.7z M75.5,71.5l13.8,0.7l0-3.4    l-13.8-1.3V71.5z M75.5,79.9L89.3,79v-3.5l-13.8,0.1V79.9z"></path></g></switch></svg>
                    </span>
                    <span>
                        {$selected_building.address}
                    </span>
                </div>
                <div on:click={()=> $selected_dashboard_component = 'properties'}
                class="flex flex-row text-xl text-gray-50 font-semibold mt-2 pt-2 pb-20 cursor-pointer items-center">
                  <span>
                        <svg class="w-8 fill-current" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><g><path d="M63.4,16.9c0.8-0.8,0.8-2,0-2.8c-0.8-0.8-2-0.8-2.8,0L28.7,45.9c-1.4,1.4-2.1,3.2-2.1,5.1s0.7,3.7,2.1,5.1L60.6,88   c0.4,0.4,0.9,0.6,1.4,0.6s1-0.2,1.4-0.6c0.8-0.8,0.8-2,0-2.8L31.5,53.3c-0.6-0.6-0.9-1.4-0.9-2.3s0.3-1.7,0.9-2.3L63.4,16.9z"></path></g></svg>
                  </span>
                  <span>
                        Back
                  </span>  
                </div>
            </div>
            <div class="pt-4 flex flex-row flex-grow gap-x-3 md:justify-end items-center pb-10 md:pb-2">
                <div title="Outdoor temperature">
                    <svg class="w-24 fill-current text-gray-400" version="1.1" x="0px" y="0px" viewBox="0 0 70 70" style="enable-background:new 0 0 70 70;" xml:space="preserve"><g><path d="M55.60938,33.1062c-1.0293,0-2.04102,0.13818-3.01953,0.41113c-0.99023-5.20605-5.53906-9.02734-10.93359-9.02734   c-2.13171,0-4.13,0.60291-5.83447,1.64819c-2.6521-3.83539-6.95471-6.10522-11.66748-6.10522   c-7.8418,0-14.2207,6.37939-14.2207,14.22021c0,2.37622,0.59863,4.70227,1.72559,6.77527   C9.64331,42.63763,8.3457,45.1106,8.3457,47.88452c0,4.83496,3.93652,8.76807,8.77539,8.76807h19.36426   c1.60791,0,3.1626-0.44794,4.52026-1.27246h14.60376c6.14258,0,11.14063-4.99414,11.14063-11.1333   C66.75,38.10376,61.75195,33.1062,55.60938,33.1062z M11.43359,34.25317c0-7.01416,5.70605-12.72021,12.7207-12.72021   c4.21924,0,8.05542,2.04828,10.42664,5.48352c-1.85083,1.51898-3.2113,3.63031-3.7782,6.09216   c-0.55139-0.01331-1.08643,0.02045-1.60938,0.08612c-1.09888-0.48157-2.26563-0.73505-3.47656-0.73505   c-4.07324,0-7.55469,2.75879-8.51758,6.65039c-0.02637-0.00049-0.05176-0.00049-0.07813-0.00049   c-1.52625,0-2.96167,0.39313-4.21326,1.08118C11.9436,38.36871,11.43359,36.33191,11.43359,34.25317z M17.12109,55.15259   c-4.01172,0-7.27539-3.26025-7.27539-7.26807c0-4.01123,3.26367-7.2749,7.27539-7.2749c0.19531,0,0.39844,0.00488,0.58789,0.02832   c0.39453,0.05029,0.76465-0.22314,0.83203-0.61914c0.59277-3.51074,3.61035-6.05908,7.17578-6.05908   c3.74789,0,6.8304,2.86983,7.22461,6.48291c0.02441,0.22998,0.1543,0.43506,0.35059,0.55664   c0.19824,0.12207,0.4375,0.14648,0.65527,0.06543c0.81543-0.30176,1.66992-0.45508,2.53809-0.45508   c4.01172,0,7.27539,3.26367,7.27539,7.2749c0,4.06219-3.31014,7.26807-7.27539,7.26807H17.12109z M55.60938,53.88013h-12.7207   c1.34297-1.76871,2.37207-3.05863,2.37207-5.99561c0-4.83838-3.93652-8.7749-8.77539-8.7749   c-0.74512,0-1.48145,0.09326-2.19824,0.27881c-0.40023-1.85022-1.50083-3.60735-2.79492-4.74561   c0.32617-0.03564,0.60059-0.28418,0.65723-0.62109c0.43396-2.57867,1.85754-4.76233,3.84241-6.19989   c0.05969-0.03485,0.11926-0.06934,0.16687-0.11884c1.56616-1.08417,3.46338-1.71301,5.49756-1.71301   c4.93457,0,9.05078,3.69385,9.57617,8.59277c0.02539,0.22998,0.1543,0.43555,0.35059,0.55713   c0.19727,0.12256,0.44043,0.14697,0.65527,0.06641c1.07715-0.39844,2.21191-0.6001,3.37109-0.6001   c5.31543,0,9.64063,4.32471,9.64063,9.64063C65.25,49.55884,60.9248,53.88013,55.60938,53.88013z"></path><path d="M23.40625,14.09741v2.92285c0,0.41406,0.33594,0.75,0.75,0.75s0.75-0.33594,0.75-0.75v-2.92285   c0-0.41406-0.33594-0.75-0.75-0.75S23.40625,13.68335,23.40625,14.09741z"></path><path d="M37.87891,19.47095l-2.06641,2.06689c-0.29297,0.29297-0.29297,0.76758,0,1.06055   c0.29308,0.29307,0.76757,0.29298,1.06055,0l2.06641-2.06689c0.29297-0.29297,0.29297-0.76758,0-1.06055   S38.17188,19.17798,37.87891,19.47095z"></path><path d="M4,35.00464h2.92188c0.41406,0,0.75-0.33594,0.75-0.75s-0.33594-0.75-0.75-0.75H4c-0.41406,0-0.75,0.33594-0.75,0.75   S3.58594,35.00464,4,35.00464z"></path><path d="M9.37402,19.47144c-0.29297,0.29297-0.29297,0.76758,0,1.06055l2.06641,2.06641c0.29307,0.29307,0.76757,0.29298,1.06055,0   c0.29297-0.29297,0.29297-0.76758,0-1.06055l-2.06641-2.06641C10.1416,19.17847,9.66699,19.17847,9.37402,19.47144z"></path></g></svg>
                </div>
                <div class="h-10 text-2xl text-gray-300 font-medium">
                    {outdoor_temp || '--'} °F
                </div>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-x-5 gap-y-2 text-sm md:absolute -bottom-8 left-8 font-medium">
            <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Leaseholder name</div>
                <div class="text-gray-600">
                    <input type="text" bind:value={leaseholder_filter} on:keyup={() => handleLeaseholderFilter()} 
                    placeholder="e.g. Andy Warhol"
                    class="py-2 px-2 bg-white box-border w-48 rounded-sm focus:outline-none">
                </div>
            </div>
            <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Occupancy status</div>
                <div class="w-full text-gray-600 filter-theme cursor-pointer">
                    <Select items={occupancy_options} value={occupancy_options[0]} isSearchable={false} on:select={handleOccupancySelect} on:clear={handleOccupancyClear} />
                </div>
            </div>
            <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Alert</div>
                <div class="w-full text-gray-600 filter-theme cursor-pointer">
                    <Select items={alert_options} value={alert_options[0]} isSearchable={false} on:select={handleAlertSelect} on:clear={handleAlertClear} />
                </div>
            </div>
        </div>
    </div>
    <div class="px-2 md:px-8 py-12 bg-gray-50 rounded-br-2xl flex flex-col flex-grow text-sm md:text-md">
        <div class="grid grid-cols-2 md:grid-cols-6 text-white apartments-grid gradient rounded-md mt-4 px-4 py-2 cursor-pointer gap-x-4 font-semibold">
            <div class="">
                Apt.
            </div>
            <div class="hidden md:block">
                Lease holder
            </div>
            <div>
                Status
            </div>
            <div class="hidden md:block">
                Temp.limits
            </div>
            <div class="hidden md:block">
                Boiler status
            </div>
            <div class="hidden md:block">
                &nbsp;
            </div>
        </div>
        {#each apartments as apartment, index (apartment.id) }
            {#if troubleshooting_blocks[index]}
                    <Troubleshooting boiler_id={apartment?.boiler?.id} on:close={() => troubleshooting_blocks[index] = false} />
            {/if}
        <div on:click={() => toggleRawDropdown(index)}
        class="grid grid-cols-2 md:grid-cols-6 apartments-grid bg-white items-center rounded-md mt-4 px-4 py-2 cursor-pointer gap-x-4 shadow-lg text-sm md:text-md">
            <div class="font-semibold flex flex-row gap-x-3">
                <span>
                    {apartment.name}
                </span>
            </div>
            <div class="hidden md:block">
                {apartment.leaseholder}
            </div>
            <div>
                {#if vacant_popup_items[index]}
                    <ConfirmPopup
                    note={'This action will remove all tenants from this apartment. Thermostats will be set to vacant temperature'}
                    on:confirm={()=> makeApartmentVacant(apartment.id, index)} 
                    on:cancel={()=> vacant_popup_items[index] = false } />
                {/if}
                {#if !apartment.is_vacant}
                <div on:click|stopPropagation={() => vacant_popup_items[index] = true }
                title="Make vacant" class="flex flex-row items-center gap-x-2">
                    <span>Occupied</span>
                    <div>
                        <svg class="w-5 fill-current text-green-500" version="1.1" x="0px" y="0px" viewBox="0 0 91 91" enable-background="new 0 0 91 91" xml:space="preserve"><g><g><g><path fill-rule="evenodd" clip-rule="evenodd" d="M89.719,13.891c-2.408-4.984-8.357-7.051-13.287-4.619     c-12.396,6.121-24.75,18.391-36.717,36.47c-1.742,2.637-3.348,5.197-4.797,7.611c-2.111-2.949-4.518-5.881-7.213-8.791     c-5.99-6.467-11.332-10.478-11.557-10.646c-4.41-3.297-10.633-2.359-13.898,2.102c-3.264,4.457-2.33,10.74,2.082,14.042     c0.162,0.121,16.514,12.662,20.818,27.484c1.162,4.002,4.664,6.861,8.783,7.18c0.254,0.014,0.506,0.023,0.756,0.023     c3.834,0,7.359-2.242,9.002-5.791c0.049-0.105,4.906-10.555,12.705-22.293c9.797-14.752,19.74-24.898,28.756-29.349     C90.086,24.879,92.131,18.87,89.719,13.891z"></path></g></g></g></svg>           
                    </div>
                </div>
                {:else}
                <div title="Add tenants" on:click|stopPropagation={() => item_tenants[index] = true} class="flex flex-row items-center gap-x-2">
                    <span>Vacant</span>
                    <div>
                        <svg class="w-7 transform -rotate-90 fill-current text-yellow-600" version="1.1" x="0px" y="0px" viewBox="0 0 96 96" enable-background="new 0 0 96 96" xml:space="preserve"><g><path d="M48,8c-8.699,0-15.751,7.053-15.751,15.752c0,7.486,9.704,13.72,9.704,13.72   c1.389,0.892,2.523,2.972,2.523,4.622v21.088c0,1.65-0.906,3-2.014,3s-2.607,0.593-3.332,1.316s-1.316,1.563-1.317,1.862   s0.347,0.893,0.77,1.315s0.424,1.115,0.001,1.538c-0.424,0.423-0.77,1.015-0.771,1.314s0.347,0.893,0.77,1.315   s0.424,1.116,0.001,1.539c-0.424,0.423-0.77,1.015-0.771,1.314s0.347,0.892,0.77,1.314s0.424,1.116,0.001,1.539   c-0.053,0.053-0.1,0.114-0.15,0.172c-0.35,0.4-0.619,0.881-0.62,1.143c0,0.077,0.04,0.19,0.11,0.326   c0.203,0.396,0.668,0.997,1.207,1.535c0.725,0.724,2.225,1.316,3.332,1.316s2.014,0.035,2.014,0.078s0.663,1.254,1.473,2.691   c0,0,0.105,0.188,2.051,0.188s2.053-0.188,2.053-0.188c0.809-1.438,1.471-3.964,1.471-5.614V42.094c0-1.65,1.137-3.729,2.525-4.622   c0,0,9.701-6.233,9.701-13.72C63.75,15.053,56.699,8,48,8z M48,30.84c-3.915,0-7.088-3.174-7.088-7.088s3.173-7.088,7.088-7.088   c3.914,0,7.088,3.174,7.088,7.088S51.914,30.84,48,30.84z"></path></g></svg>
                    </div>
                </div>
                {/if}
            </div>
            <div class="hidden md:block">
                <span>
                    {#if apartment.tlimits_is_on}
                        {apartment.min_temp || ''} — {apartment.max_temp || ''} °F
                    {:else}
                        Full range
                    {/if}
                </span>
            </div>
            <div class="flex-row items-center hidden md:flex px-4 gap-x-2">
                {#if apartment.controller_sn}
                    {#await getEndSwitchStatus(apartment)}
                        ...
                    {:then value}
                        {#if value?.online_status === false}
                        <div in:fade title="Controller is offline">
                            <svg class="w-5 fill-current text-gray-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g><path d="M50.048,61.368c4.418,0,8.421,1.798,11.323,4.699l4.691-4.691c-3.373-3.372-7.801-5.686-12.737-6.404l-6.799,6.8   C47.661,61.516,48.837,61.368,50.048,61.368z"></path><path d="M43.477,70.818l6.571,6.572l6.571-6.572c-1.681-1.683-4.006-2.723-6.571-2.722C47.482,68.097,45.158,69.136,43.477,70.818z   "></path><path d="M50.048,41.544c-9.882-0.001-18.845,4.02-25.336,10.51l4.693,4.691c3.758-3.757,8.535-6.491,13.872-7.764l7.421-7.422   C50.481,41.557,50.266,41.544,50.048,41.544z"></path><path d="M70.692,56.746l4.69-4.691c-3.255-3.255-7.133-5.888-11.435-7.705l-5.167,5.166C63.329,50.944,67.401,53.454,70.692,56.746   z"></path><path d="M50.048,28.319c-13.528,0-25.797,5.503-34.682,14.39l4.692,4.692c7.684-7.684,18.292-12.442,29.991-12.443   c2.286,0,4.527,0.187,6.717,0.537l5.605-5.606C58.432,28.865,54.303,28.319,50.048,28.319z"></path><path d="M68.905,39.392c4.137,2.062,7.897,4.771,11.134,8.006l4.69-4.691c-3.223-3.224-6.897-5.995-10.911-8.228L68.905,39.392z"></path></g><path d="M50.277,4.35C25.106,4.35,4.627,24.829,4.627,50c0,25.172,20.479,45.65,45.65,45.65c25.172,0,45.65-20.479,45.65-45.65  C95.928,24.829,75.449,4.35,50.277,4.35z M50.277,10.936c9.419,0,18.069,3.351,24.823,8.923L20.136,74.823  C14.564,68.069,11.213,59.419,11.213,50C11.213,28.46,28.738,10.936,50.277,10.936z M50.277,89.063  c-9.418,0-18.068-3.35-24.821-8.921L80.42,25.179c5.571,6.753,8.921,15.403,8.921,24.821C89.341,71.54,71.817,89.063,50.277,89.063z  "></path></svg>
                        </div>
                        {:else if value?.endswitch === 1 }
                        <div in:fade title="Active">
                            <svg class="w-4 fill-current text-yellow-600" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                                <g>
                                <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                                </path>
                                </g>
                            </svg>
                        </div>
                        {:else if value?.endswitch === 0 }
                        <div in:fade title="Standby">
                            <svg class="w-4 fill-current text-gray-400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                                <g>
                                <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                                </path>
                                </g>
                            </svg>
                        </div>
                        {/if}
                        <div title="System temperature" class="font-semibold">
                            <span class="text-yellow-600 ">  {value?.systemp > -100 && value?.online_status ? value?.systemp: '--'}</span>  °F
                        </div>
                    {/await}
                {:else}
                    <div title="Apartment doesn't have boiler or controller connected">
                        <svg class="w-5 fill-current text-gray-400" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M50,5.5C25.424,5.5,5.5,25.424,5.5,50c0,24.577,19.924,44.5,44.5,44.5c24.577,0,44.5-19.923,44.5-44.5  C94.5,25.424,74.577,5.5,50,5.5z M50,16.5c6.971,0,13.442,2.131,18.804,5.774L22.274,68.805C18.631,63.443,16.5,56.971,16.5,50  C16.5,31.499,31.499,16.5,50,16.5z M50,83.5c-6.912,0-13.334-2.095-18.669-5.683l46.486-46.486C81.405,36.666,83.5,43.088,83.5,50  C83.5,68.501,68.501,83.5,50,83.5z"></path></svg>
                    </div>
                {/if}
            </div>
            <div
            class="justify-end items-center px-2 hidden md:inline-flex">
            <svg class="fill-current w-5 transition transform text-gray-500" class:rotate-180={item_details[index]} viewBox="0 0 668 375" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                <g>
                    <path class="fil0" d="M363 363l293 -292c16,-17 16,-43 0,-59 -16,-16 -43,-16 -59,0l-263 263 -263 -263c-17,-16 -43,-16 -59,0 -16,16 -16,42 0,59l292 292c17,16 43,16 59,0z">
                    </path>
                </g>
            </svg>
            </div>
        </div>
        {#if item_details[index]}
        <div class="mt-2 shadow-sm bg-white p-5" in:slide>
            <Rooms 
                apartment={apartment} 
                temp_range={[apartment.min_temp, 
                apartment.max_temp]} 
                on:change={() => loadApartments()}
            />
            <div class="flex flex-row gap-x-6 mt-6 text-sm">
                {#if apartment.boiler && !(apartment.controller_type === 'MN')}
                <div>
                    <button on:click={()=> troubleshooting_blocks[index] = !troubleshooting_blocks[index]}
                    class="flex flex-row items-center gap-x-3 px-4 py-2 shadow-md active:shadow-sm bg-gray-100 text-gray-700">
                        <span>
                            Show detailed report
                        </span>
                    </button>
                </div>
                {/if}
                <div>
                    <button on:click={()=> toggleDropdownView(index)}
                    class="flex flex-row items-center gap-x-3 px-4 py-2 shadow-md active:shadow-sm bg-gray-100 text-gray-700">
                        <span>
                            Tenants
                        </span>
                    </button>
                </div>
            </div>
        </div>
        {/if}
        {#if item_tenants[index]}
        <div class="mt-2 shadow-sm bg-white p-5" in:slide>
            <Tenants 
                apartment={apartment} 
                on:change={() => loadApartments()}
            />
            <div class="flex flex-row gap-x-6 mt-6 text-sm">
                <button on:click={()=> toggleDropdownView(index)}
                    class="flex flex-row items-center gap-x-3 px-4 py-1 shadow-md active:shadow-sm bg-gray-100 text-gray-700">
                        <span>
                           Back to troubleshooting
                        </span>
                </button>
            </div>
        </div>
        {/if}
    {/each}
    </div>

</div>


<style>
    /* .apartments-grid {
        grid-template-columns: 4rem 15rem 15rem auto auto 4rem;
    } */
    .gradient {
        background: #2C3E50;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #4CA1AF, #2C3E50);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #4CA1AF, #2C3E50); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

    }
    .filter-theme {
        --itemHoverBG: #cdffee;
        --itemIsActiveBG: #59bae7;
    }
    /* .header-gradient {

    } */
</style>