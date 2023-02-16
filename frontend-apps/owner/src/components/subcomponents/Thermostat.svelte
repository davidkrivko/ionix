<script>
export let thermostat;
import jQuery from 'jquery';
import roundSlider from 'round-slider';
import axios from 'axios';
import { onMount } from 'svelte';
import { fade } from 'svelte/transition';
import { getCsrfCookieValue } from '../../lib/utils';
import Schedule from './Schedule.svelte';

let zone = thermostat.zone;
let room_temp;
let set_temp = thermostat?.set_temperature;
let last_set_temp = thermostat?.last_set_temperature; // value saved before switching off and setting set_temp to 39*
let status = thermostat?.status; // call for heat status, 1 - if calling for heat, 0 - not (set / below room temp)
let controller_online = false;
let active = false; // inactivated by backend logic or request/response data absence
let endswitch; // zone status (pumps working or not)
let switched_on = false; // disabled by poweroff button component
let scheduled_override = thermostat?.scheduled_override; //if override happened show related image


let schedule_popup = false;
let thermostat_input;
let freeze;

onMount(() => {

    getThermostatSetPoint(); // fetches last set_temp from Django model
    getThermostatData(); // fetches data from thermostat data IoT db
    fetchThermostatOnlineStatus(); // fetches data from online_status Redis stram

    if (zone) {
      fetchRelatedIoniqData();
      fetchIoniqOnlineStatus(); // getches controller online status based on thermostat serial
    }
  
    mountRoundSlider(thermostat_input);
    freeze = true;

    let thermostat_data_interval = setInterval(()=> getThermostatData(), 10000);
    let thermostat_status_interval =  setInterval(()=> fetchThermostatOnlineStatus(), 5000);
    let ioniq_endswitch_interval = setInterval(() => fetchRelatedIoniqData(), 10000);
    let ioniq_status_interval = setInterval(() => fetchIoniqOnlineStatus(), 5000);

    return () => {
      clearInterval(thermostat_data_interval);
      clearInterval(thermostat_status_interval);
      clearInterval(ioniq_endswitch_interval);
      clearInterval(ioniq_status_interval);
    }
});


const changeSetValue = (e) => {
  set_temp = e.value;
  // Force call for heat status if condition checks
  if (set_temp > room_temp) status = 1;
  saveSetPointTemp();

}

function updateSliderValue() {
  jQuery(thermostat_input).roundSlider(
    'setValue', set_temp
  )
}

function mountRoundSlider(node) {
        jQuery(node).roundSlider({
            radius: 72,
            width: 16,
            circleShape: "half-top",
            sliderType: "min-range",
            // mouseScrollAction: true,
            editableTooltip: false,
            value: set_temp,
            handleSize: "+12",
            min: 40,
            max: 90,
            change: changeSetValue,
        })
    }

async function getThermostatData() {
  
  const endpoint = `/api/devices/thermostats/custom/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": thermostat.serial_num
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
            const thermostat_data = response.data.data;
            status = thermostat_data[0].status;
            room_temp = thermostat_data[0].roomtemp;
            set_temp = thermostat_data[0].settpoint;
            if (switched_on === false) return;
            validateThermostatStatus(); 
        }
    } catch(error) {
            console.log(error)
    }
};



async function getThermostatSetPoint(last_temp_only = false) {
  
const endpoint = `/api/devices/thermostat/setpoint/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": thermostat.serial_num
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
        console.log("Thermostat data", response.data.data)
        const response_date = response.data.data;
        if (last_temp_only) {
          last_set_temp = response_date.last_set_temperature;
        } else {
          set_temp = response_date.set_temperature;
          last_set_temp = response_date.last_set_temperature;
          switched_on = response_date.status;
          switched_on === false ? freeze = true : freeze = false;
          scheduled_override = response_date.scheduled_override;
          updateSliderValue();
        }
        }
    } catch(error) {
          console.log(error)
    }
};


async function saveSetPointTemp() {

    try {
    const endpoint = '/api/devices/thermostat/set/';
    const csrfcookie = getCsrfCookieValue();
    console.log("set_temp before setting point ", set_temp)
    const data = {
      "thermostat_sn": thermostat.serial_num,
      "set_temperature": set_temp,
      "status": switched_on,
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

async function fetchThermostatOnlineStatus() {

    try {
    const endpoint = '/api/devices/thermostat/status/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": thermostat.serial_num
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
          console.log("Thermostat status response for ", thermostat.serial_num, response.data)
          active = res;
        }
    } catch(error) {
          console.log(error)
    }
};

async function fetchIoniqOnlineStatus() {
    // do nothing if thermostat wasn't connected to a heating zone
    if (zone === null) return;
    try {
    const endpoint = '/api/devices/thermostat/controller/status/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": thermostat.serial_num
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
          console.log("Controller status response for ", thermostat.serial_num, response.data)
          controller_online = res;
          console.log("controller_online", controller_online)
        }
    } catch(error) {
          console.log(error)
}
};


async function fetchRelatedIoniqData() {
    // do nothing if thermostat wasn't connected to a heating zone
    if (zone === null) return;
    
    try {
    const endpoint = '/api/devices/thermostat/iodata/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": thermostat.serial_num
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
          endswitch = response.data.data.endswitch;          
        }
    } catch(error) {
          console.log(error)
    }
};


function validateThermostatStatus() {
  freeze = false;
  if (status === 2) {
    freeze = true;
  }
  if (active === false) {
    freeze = true;
  }
}

function toogleRangeSlider() {
  if (freeze) {
    jQuery(thermostat_input).roundSlider('disable')
  } else {
    jQuery(thermostat_input).roundSlider('enable')
  }
}

function toggleThermostat() {

  if (switched_on === true) {
    switched_on = false;
    set_temp = 39;
    getThermostatSetPoint(true);
    saveSetPointTemp();

  } else {
    switched_on = true;
    // getThermostatSetPoint(true);
    set_temp = last_set_temp;
    saveSetPointTemp();
  }
  updateSliderValue();
  freeze = !switched_on;
}

$: toogleRangeSlider(), freeze;

</script>


{#if schedule_popup}
  <Schedule device_id={thermostat.id} device_type="thermostats" on:close={() => schedule_popup = false} />
{/if}




<div class="mt-4 relative mx-auto">
  <div class="cursor-pointer absolute -mt-4" class:text-purple-400={thermostat.scheduled_override} 
  title="{thermostat.scheduled_override ? 'Thermostat setpoint has been overriden by scheduling' : 'Schedule settings'}" 
  on:click={()=> schedule_popup = true}>
      <svg class="fill-current w-6" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M37.6,48.8c0,0.8-0.7,1.5-1.5,1.5h-5.6c-0.8,0-1.5-0.7-1.5-1.5v-5.6c0-0.8,0.7-1.5,1.5-1.5h5.6c0.8,0,1.5,0.7,1.5,1.5V48.8z   M49.4,43.2c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V43.2z   M61.2,43.2c0-0.8-0.7-1.5-1.5-1.5H54c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V43.2z   M37.6,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M49.4,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M59.7,53.1H54c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C61.2,53.8,60.5,53.1,59.7,53.1z   M24.3,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C25.8,65.3,25.2,64.6,24.3,64.6z   M25.8,54.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5V54.6z   M47.9,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C49.4,65.3,48.7,64.6,47.9,64.6z   M36.1,64.6h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5h5.6c0.8,0,1.5-0.7,1.5-1.5v-5.6C37.6,65.3,36.9,64.6,36.1,64.6z   M71.4,50.3c0.8,0,1.5-0.7,1.5-1.5v-5.6c0-0.8-0.7-1.5-1.5-1.5h-5.6c-0.8,0-1.5,0.7-1.5,1.5v5.6c0,0.8,0.7,1.5,1.5,1.5H71.4z   M13.5,85.5h42.8c-0.7-2.2-1.1-4.5-1.1-6.8H13.5c-1.1,0-2-0.9-2-2V36.4h67.1v18.8c2.4,0,4.7,0.4,6.8,1V22.2c0-4.9-4-8.8-8.8-8.8  h-9.9V7.9c0-1.8-1.4-3.2-3.2-3.2h-5c-1.8,0-3.2,1.4-3.2,3.2v5.5H34.9V7.9c0-1.8-1.4-3.2-3.2-3.2h-5c-1.8,0-3.2,1.4-3.2,3.2v5.5h-9.9  c-4.9,0-8.8,4-8.8,8.8v54.4C4.6,81.5,8.6,85.5,13.5,85.5z M95.4,78.4c0,9.3-7.6,16.9-16.9,16.9c-9.3,0-16.9-7.6-16.9-16.9  c0-9.3,7.6-16.9,16.9-16.9C87.8,61.5,95.4,69.1,95.4,78.4z M87,74c0-0.5-0.2-1.1-0.6-1.4c-0.8-0.8-2.1-0.8-2.9,0l-7.3,7.3l-2.8-2.8  c-0.8-0.8-2.1-0.8-2.9,0c-0.4,0.4-0.6,0.9-0.6,1.4c0,0.5,0.2,1,0.6,1.4l4.2,4.2c0.8,0.8,2.1,0.8,2.9,0l8.8-8.8  C86.8,75.1,87,74.6,87,74z"></path></svg>
  </div>
  <div id="slider" class="rslider" bind:this={thermostat_input}></div>
    <div class="thermostat">
        <div class="ring" class:ring-active={!freeze} class:ring-hot={!freeze && status === 1}>
            <div class="bottom_overlay"></div>
        </div>
        <div class="control">
            <div class="temp_outside" title="Room temperature">{ active ? room_temp : '--'}°</div>
            <!-- <div class="temp_room" title="Set temperature"> <span> °</span></div> -->
            {#if zone}
            <div class="indicator" in:fade>
              <svg height="20px" width="20px" fill={endswitch === 1 && controller_online === true ? '#ff9a0d' : '#7a7a7a'}
              xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
              version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
                <title>Heating status: {endswitch === 1 ? 'On' : endswitch === 0 ? 'Off' : '--'}</title>
                <path d="M67.1,37.9c-1.4-12.9-13-29-23.6-33.2c1.9,10.1-2.4,22.5-16.3,41.3c0.1-1.4,0.5-8.4-3.4-14.8C24.9,38.4,14.8,51,13.3,64  c-1.5,13,7.2,23.2,20.4,30.7l0.4,0C24,81.4,37.6,61,46.9,56.8c-2.6,6.4,2.9,16,6.4,18.2c-1.7-5.4,0.8-8.2,2.1-9.6  c0.7,10.4,16.3,13.8,8.7,28.7c11.3-6.6,19-16.9,21.9-27.6c2.9-10.9-1.8-29.4-17.3-44.9C70.4,24.1,72.4,33.7,67.1,37.9z"></path>
              </svg>  
            </div>
            {/if}
        </div>
    </div>
    <div class="absolute w-8 -right-2 bottom-0 cursor-pointer" on:click={() => toggleThermostat()}>
      <svg class="fill-current text-gray-400 transform transition-colors" class:text-green-500={switched_on===true}
      x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
      <title> Turn {switched_on ? 'off' : 'on'} </title>
      <switch><g><path d="M50,2.5L50,2.5C23.8,2.5,2.5,23.8,2.5,50l0,0c0,26.2,21.3,47.5,47.5,47.5l0,0c26.2,0,47.5-21.3,47.5-47.5l0,0    C97.5,23.8,76.2,2.5,50,2.5z M45.7,24.2c0-2.4,1.9-4.3,4.3-4.3s4.3,1.9,4.3,4.3v21.6c0,2.4-1.9,4.3-4.3,4.3s-4.3-1.9-4.3-4.3V24.2    z M50,78.4c-15.2,0-27.6-12.4-27.6-27.6c0-8.7,4-16.7,11-22c1.9-1.4,4.6-1,6,0.8c1.4,1.9,1,4.6-0.8,6c-4.8,3.6-7.6,9.2-7.6,15.2    c0,10.5,8.5,19.1,19.1,19.1c10.5,0,19.1-8.5,19.1-19.1c0-6-2.8-11.5-7.6-15.2c-1.9-1.4-2.3-4.1-0.8-6c1.4-1.9,4.1-2.3,6-0.8    c7,5.3,11,13.3,11,22C77.6,66,65.2,78.4,50,78.4z"></path></g></switch></svg>
    </div>
</div>


<style>

</style>