<script>

    import { onMount } from 'svelte';
    import axios from 'axios';
    import { getCsrfCookieValue } from '../../lib/utils';
    import Schedule from './Schedule.svelte';

    export let item;
    let schedule_popup;
    // let gsap;
    let sync;
    let toggle_status = false;
    let zone_active = false;
    let controller_online = false;

    onMount(() => {
    
        fetchZoneStatus();
        fetchIoniqOnlineStatus();

        const zonestatus_interval = setInterval(()=> fetchZoneStatus(), 1000*5);

        if (item.status) {
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
        const endpoint = '/api/devices/athermostat/update/';
        const csrfcookie = getCsrfCookieValue();
    
        const status = toggle_status;

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
      const endpoint = '/api/devices/athermostat/controller/status/';
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
            console.log("Analogue thermostat controller status response for ", item.serial_num, response.data)
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
      "device_type": "analogue",
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
    
    {#if schedule_popup}
      <Schedule device_id={item.id} device_type="analogue-thermostats" on:close={() => schedule_popup = false} />
    {/if}

    <div class="mt-4 relative">
      <div class="cursor-pointer absolute -mt-4" class:text-purple-400={item.scheduled_override} 
      title="{item.scheduled_override ? 'Heating switch state has been overriden by scheduling' : 'Schedule settings'}" 
      on:click={()=> schedule_popup = true}>
          <svg class="fill-current w-6" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M37.6,48.8c0,0.8-0.7,1.5-1.5,1.5h-5.6c-0.8,0-1.5-0.7-1.5-1.5v-5.6c0-0.8,0.7-1.5,1.5-1.5h5.6c0.8,0,1.5,0.7,1.5,1.5V48.8z   M49.4,43.2c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V43.2z   M61.2,43.2c0-0.8-0.7-1.5-1.5-1.5H54c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V43.2z   M37.6,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M49.4,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M59.7,53.1H54c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C61.2,53.8,60.5,53.1,59.7,53.1z   M24.3,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C25.8,65.3,25.2,64.6,24.3,64.6z   M25.8,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M47.9,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C49.4,65.3,48.7,64.6,47.9,64.6z   M36.1,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C37.6,65.3,36.9,64.6,36.1,64.6z   M71.4,50.3c0.8,0,1.5-0.7,1.5-1.5v-5.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5H71.4z   M13.5,85.5h42.8c-0.7-2.2-1.1-4.5-1.1-6.8H13.5c-1.1,0-2-0.9-2-2V36.4h67.1v18.8c2.4,0,4.7,0.4,6.8,1V22.2c0-4.9-4-8.8-8.8-8.8  h-9.9V7.9c0-1.8-1.4-3.2-3.2-3.2h-5c-1.8,0-3.2,1.4-3.2,3.2v5.5H34.9V7.9c0-1.8-1.4-3.2-3.2-3.2h-5c-1.8,0-3.2,1.4-3.2,3.2v5.5h-9.9  c-4.9,0-8.8,4-8.8,8.8v54.4C4.6,81.5,8.6,85.5,13.5,85.5z M95.4,78.4c0,9.3-7.6,16.9-16.9,16.9c-9.3,0-16.9-7.6-16.9-16.9  c0-9.3,7.6-16.9,16.9-16.9C87.8,61.5,95.4,69.1,95.4,78.4z M87,74c0-0.5-0.2-1.1-0.6-1.4c-0.8-0.8-2.1-0.8-2.9,0l-7.3,7.3l-2.8-2.8  c-0.8-0.8-2.1-0.8-2.9,0c-0.4,0.4-0.6,0.9-0.6,1.4c0,0.5,0.2,1,0.6,1.4l4.2,4.2c0.8,0.8,2.1,0.8,2.9,0l8.8-8.8  C86.8,75.1,87,74.6,87,74z"></path></svg>
      </div>
      <div class="cursor-pointer absolute right-1 -mt-5" title={controller_online ? 'Controller is online' : 'Controller is offline'}>
        <svg class="w-8 fill-current text-gray-400" class:text-green-600={controller_online} version="1.1" viewBox="0 0 752 752" xmlns="http://www.w3.org/2000/svg">
          <path d="m376 186.57c104.73 0 189.43 84.703 189.43 189.43s-84.707 189.43-189.43 189.43c-104.73 0-189.43-84.707-189.43-189.43 0-104.73 84.703-189.43 189.43-189.43z" fill-rule="evenodd"/>
         </svg>
      </div>

        <button bind:this={sync} on:click={()=>toggleSync()} class="sync" class:rotating={toggle_status && zone_active}>
            <i class="fas fa-sync" title="Heating zone is active"></i>
            <span class="ml-3">Turned off</span>
        </button>
    
    </div>
    
    
    
    <style>
     @import "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css";
    </style>