<script>
import { onMount } from 'svelte'; 
import axios from 'axios';
import { fade, slide } from 'svelte/transition';
import { selected_building, selected_dashboard_component } from '../stores/store';

let buildings = [];
let address_filter = '';
let name_filter = '';

onMount(()=>{
    loadBuildings();
})

async function loadBuildings() {
  try {
  const endpoint = `/api/users/owner/building/?name=${name_filter}&address=${address_filter}`;
  const response = await axios({
      url: endpoint,
      method: "get",

  });
  if(response.status === 200) {
         const res = response.data;

         buildings = res;
      }
  } catch(error) {
        console.log(error)
  }
};

function showApartments(building) {
    $selected_building = building;
    $selected_dashboard_component = 'apartments';
}
// function handleBuildingNameFilter() {
//     loadBuildings();
// }
// function handleBuildingAddressFilter() {
//     loadBuildings();
// }
</script>



<div class="flex flex-col h-full" in:fade>
    <div class="w-full gradient py-6 px-2 md:px-8 rounded-tr-2xl relative">
        <div class="text-xl md:text-3xl font-bold py-4 text-white tracking-wider pb-16">
            My Properties
        </div>
        <!-- <div class="text-xl text-gray-50 font-semibold mt-6 py-4 pb-10">
            Overview
        </div> -->
        <!-- <div class="grid grid-cols-1 lg:grid-cols-3 gap-x-5 gap-y-2 text-sm md:text-base md:absolute -bottom-8 left-8 font-medium">
            <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Building name</div>
                <div class="text-gray-600">
                    <input type="text" bind:value={name_filter} on:keyup={() => handleBuildingNameFilter()} 
                    placeholder="e.g. My first building"
                    class="py-2 px-2 bg-white box-border w-48 rounded-sm focus:outline-none">
                </div>
            </div>
            <div class="w-56 grid grid-cols-1 gap-y-2 bg-opacity-30 bg-gray-600 py-2 px-4 rounded-md text-white cursor-pointer shadow-md">
                <div>Building adress</div>
                <div class="text-gray-600">
                    <input type="text" bind:value={address_filter} on:keyup={() => handleBuildingAddressFilter()} 
                    placeholder="e.g. 132 Parklane"
                    class="py-2 px-2 bg-white box-border w-48 rounded-sm focus:outline-none">
                </div>
            </div>
        </div> -->
    </div>
    <div class="px-2 md:px-8 py-12 bg-gray-50 rounded-br-2xl flex flex-col flex-grow text-sm md:text-md">
    {#each buildings as building }
        <div on:click={() => showApartments(building)}
        class="grid grid-cols-1 divide-x-2 shadow-lg bg-white rounded-md mt-4 px-4 py-2 cursor-pointer gap-x-8 overflow-hidden">
            <div class="flex flex-row gap-x-3 px-2">
                <span>
                    <svg class="w-5 fill-current text-gray-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><switch><foreignObject requiredExtensions="http://ns.adobe.com/AdobeIllustrator/10.0/" x="0" y="0" width="1" height="1"></foreignObject><g i:extraneous="self"><path d="M11.1,60.1l10.2-2.6v4.5L11.1,64V60.1z M11.1,56.2L21.3,53v-4.5l-10.2,3.9V56.2z M24.3,93l16.6,4.4v-10l-16.6-2.2V93z     M11.1,71.7l10.2-0.6v-4.5l-10.2,1.2V71.7z M11.1,33l10.2-7.2v-4.5l-10.2,7.8V33z M11.1,25.2l10.2-8.5v-7l-10.2,9.8V25.2z     M11.1,48.5l10.2-4.5v-4.5l-10.2,5.2V48.5z M11.1,40.7l10.2-5.9v-4.5l-10.2,6.5V40.7z M11.1,79.5l10.2,0.7v-4.5l-10.2-0.1V79.5z     M61,26.6l-17.3-8.9v5.8l17.3,8L61,26.6z M24.3,8.7v5.6l4.1-3.4L24.3,8.7z M61,13.6L43.8,2.1v9.7L61,21.5L61,13.6z M61,46.2    l-17.3-5.3v5.8L61,51.1L61,46.2z M61,36.5l-17.3-7.2v5.8L61,41.2L61,36.5z M61.1,75.8H43.8v5.8l17.3-1.1V75.8z M61,56.1l-17.3-3.5    v5.8L61,61L61,56.1z M61,65.9l-17.3-1.7v5.9l17.3,0.8L61,65.9z M11.1,89.7l10.2,2.6v-7.5l-10.2-1.4V89.7z M24.3,33.2l16.6-9.5    v-5.8L24.3,28.5V33.2z M24.3,42.6l16.6-7.4v-5.8l-16.6,8.4V42.6z M24.3,23.7l16.6-11.7V2.5L24.3,16.2V23.7z M43.8,87.5v10.1    l17.3-3.6l0-8.3L43.8,87.5z M24.3,71l16.6-1v-5.8l-16.6,2V71z M24.3,80.4l16.6,1.2v-5.8l-16.6-0.1V80.4z M24.3,52.1l16.6-5.2V41    l-16.6,6.3V52.1z M24.3,61.5l16.6-3.1v-5.8l-16.6,4.2V61.5z M75.5,46.5l13.8,4.9l0-3.4l-13.8-5.7V46.5z M75.5,54.8l13.8,3.5l0-3.4    l-13.8-4.2V54.8z M75.5,38.1l13.8,6.4l0-3.4L75.5,34V38.1z M75.5,23.2v6.7l13.8,7.7l0-5L75.5,23.2z M75.5,63.1l13.8,2.1l0-3.4    l-13.8-2.8V63.1z M75.5,90.8l13.8-3l0-5.3l-13.8,1.5V90.8z M63.9,89.7l8.7,1.3V23l-8.7,4.9V89.7z M75.5,71.5l13.8,0.7l0-3.4    l-13.8-1.3V71.5z M75.5,79.9L89.3,79v-3.5l-13.8,0.1V79.9z"></path></g></switch></svg>
                </span>
                <span>
                    {building.address} 
                </span>
            </div>
        </div>
    {/each}
    </div>
</div>


<style>
    .gradient {
        background: #2C3E50;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #4CA1AF, #2C3E50);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #4CA1AF, #2C3E50); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

    }
</style>