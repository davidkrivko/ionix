<script>

import { onMount } from 'svelte';
import axios from 'axios';
import { getCsrfCookieValue } from '../../lib/utils';

export let item;

// let gsap;
let sync;

let toggle_status = false;
let zone_active = false;
let controller_online = false;

onMount(() => {

    fetchZoneStatus();
    fetchIoniqOnlineStatus();

    const zonestatus_interval = setInterval(()=> fetchZoneStatus(), 1000*5)

    if (item.status === true) {
        toggle_status = true;
        sync.classList.toggle('active')
        sync.querySelector('span').innerHTML = 'Active'
    }

    return () => {
      clearInterval(zonestatus_interval);
    }

});


async function updateStatus() {
    try {
    const endpoint = '/api/devices/heatswitch/update/';
    const csrfcookie = getCsrfCookieValue();

    const status = toggle_status === true;
            
    const data = {
      "id": item.id,
      "status": status,
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
            console.log(response.data);
        }
    } catch(error) {
              console.log(error)
    }
};

async function fetchIoniqOnlineStatus() {
      try {
      const endpoint = '/api/devices/heatwswitch/controller/status/';
      const csrfcookie = getCsrfCookieValue();
      const data = {
        "sn": item.serial_num
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
            const res = response.data.data;
            console.log("Heat switch controller status response for ", item.serial_num, response.data)
            controller_online = res;
            console.log("controller_online", controller_online)
          }
      } catch(error) {
            console.log(error)
  }
  };

async function fetchZoneStatus(serial_num) {
  if (toggle_status === false) return;
    try {
    const endpoint = '/api/devices/zonestatus/';
    const csrfcookie = getCsrfCookieValue();

    const data = {
      "sn": item.serial_num,
      "device_type": "heat_switch",
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
          response.data.data === 1 ? zone_active = true: zone_active = false;
        }
    } catch(error) {
          console.log(error)
    }
};


const toggleActive = (element) => {
  element.classList.toggle('active')
  toggle_status = !toggle_status;
  updateStatus();
}


const toggleSync = () => {
  toggleActive(sync)
  if (sync.classList.contains('active')) {
      sync.querySelector('span').innerHTML = 'Active'
      } 
  else {
    sync.querySelector('span').innerHTML = 'Turned off'
  }
}

</script>


<div class="mt-4 relative">
  <div class="cursor-pointer absolute right-1 -mt-5" title={controller_online ? 'Controller is online' : 'Controller is offline'}>
    <svg class="w-8 fill-current text-gray-400" class:text-green-600={controller_online} version="1.1" viewBox="0 0 752 752" xmlns="http://www.w3.org/2000/svg">
      <path d="m376 186.57c104.73 0 189.43 84.703 189.43 189.43s-84.707 189.43-189.43 189.43c-104.73 0-189.43-84.707-189.43-189.43 0-104.73 84.703-189.43 189.43-189.43z" fill-rule="evenodd"/>
     </svg>
  </div>
    <button bind:this={sync} on:click={()=>toggleSync()} class="sync" class:rotating={toggle_status && zone_active}>
          <i class="fas fa-sync" title="Heating activity"></i>
        <span class="ml-3">Turned off</span>
    </button>
</div>



<style>
 @import "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css";
</style>