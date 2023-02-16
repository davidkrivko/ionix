<script>
import { onMount } from 'svelte'; 
import axios from 'axios';
import { fade, slide } from 'svelte/transition';
import OutdoorTemp from './shared/OutdoorTemp.svelte';
import Thermostat from './subcomponents/Thermostat.svelte';
import SimpleSwitch from './subcomponents/SimpleSwitch.svelte';
import AnalogueThermostat from './subcomponents/AnalogueThermostat.svelte';

import { getCsrfCookieValue } from '../lib/utils';

let rooms_data = [];

onMount(()=>{
    loadRooms();
})

async function loadRooms() {
  try {
  const endpoint = `/api/users/owner/rooms/all/`;
  const response = await axios({
      url: endpoint,
      method: "get",

  });
  if(response.status === 200) {
        rooms_data = response.data;
      }
  } catch(error) {
        console.log(error)
  }
};

async function updateRoomName(e, room_id) {
    try {
        const endpoint = '/api/properties/room/changename/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
        "id": room_id,
        "name": e.target.value,
        }
        const response = await axios({
            url: endpoint,
            method: "post",
            data: data,
            headers: {
            'X-CSRFToken': csrfcookie
            }

        });
        // if(response.status === 200) {
        //     }
    } catch(error) {
            console.log(error)
    }

    // e.target.disabled = true;
}
</script>


<div class="mx-auto" in:fade>

    <OutdoorTemp />

    <div class="flex flex-col md:flex-row justify-center items-start mt-10 flex-wrap">

    {#each rooms_data as room }
        <div class="p-4 flex flex-col justify-center content-center">
            <div class="flex flex-row justify-center">
                <div>
                    <textarea class="px-2 py-0.5 h-8 text-center font-semibold" 
                    on:change={(e) => updateRoomName(e, room.id)}
                    on:keyup|preventDefault={(e) => {if (e.key === 'Enter') updateRoomName(e, room.id)}}
                    on:keydown={(e) => {if (e.key === 'Enter') e.preventDefault(), e.target.blur();}}
                    autocorrect="false" autocomplete="false">{room.name}</textarea>
                </div>
            </div>

            <!-- <div class="w-full h-0.5 bg-gray-200 my-1"></div> -->
            <div class="mx-auto grid grid-cols-1 gap-y-4 mt-2">
                {#if room.thermostat !== null}
                <Thermostat thermostat={room.thermostat} />
                {/if}
                {#if room.heat_switch !== null}
                <SimpleSwitch item={room.heat_switch} />
                {/if}
                {#if room.analogue_thermostat !== null}
                <AnalogueThermostat item={room.analogue_thermostat} />
                {/if}
            </div>
        </div>
    {:else} 

        <div class="mx-auto flex flex-col items-center mt-12">
            <span>No device configuration found.</span>
            <!-- <div class="w-14">
            <svg version="1.1" id="L6" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
            viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve">
                <rect fill="none" stroke="#000" stroke-width="4" x="25" y="25" width="50" height="50">
                <animateTransform
                attributeName="transform"
                dur="0.5s"
                from="0 50 50"
                to="180 50 50"
                type="rotate"
                id="strokeBox"
                attributeType="XML"
                begin="rectBox.end"/>
                </rect>
                <rect x="27" y="27" fill="#000" width="46" height="50">
                <animate
                attributeName="height"
                dur="1.3s"
                attributeType="XML"
                from="50" 
                to="0"
                id="rectBox" 
                fill="freeze"
                begin="0s;strokeBox.end"/>
                </rect>
            </svg>
            </div> -->
        </div>
    {/each}
    </div>
</div>

<style>

@import "https://cdnjs.cloudflare.com/ajax/libs/roundSlider/1.6.1/roundslider.min.css";
@import "../assets/thermostat.css";

textarea {
    -webkit-appearance: none;
    overflow: hidden;
    overflow-wrap: break-word;
    appearance: none;
    background: transparent;
    resize: none;
    min-height: 16px;
    outline: none;
    transition-duration: 1s;
    transition-property: color, border;
    transition-timing-function: ease;
    border-radius: 3px;
    font-size: 18px;
}

textarea:focus {
    border-bottom: 2px solid rgb(228, 228, 228);
    padding-bottom: 4px;
    /* background-color: white; */
    color: #000;
}
</style>