<script>
export let room;

import axios from "axios";
import { getCsrfCookieValue } from '../../lib/utils';
import { onMount } from 'svelte';

onMount(() => {
    showDeviceInfo();
    checkIfOnline(room.thermostat.serial_num);
    const online_interval = setInterval(() => checkIfOnline(room.thermostat.serial_num), 10000);
    
    return () => {
        clearInterval(online_interval);
    }
});

let online = false;
let room_temp;
let status = false;

// const markerNameA = "start-of-status-request";

async function showDeviceInfo() {
    if (room.thermostat) {
        const res = await getThermostatData(room.thermostat);
        if (res[0].roomtemp < 0) {
            room_temp = undefined;
        } else {
            room_temp = res[0].roomtemp;
            if(res[0].status === 1) {
                status = true;
            } else {
                status = false;
            }
        }
    }
}

async function getThermostatData(thermostat) {

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
            console.log("Thermostat data", thermostat_data)
            return thermostat_data;

        }
    } catch(error) {
            console.log(error)
    }
};


async function checkIfOnline(thermostat_sn) {
        try {
        const endpoint = '/api/devices/thermostat/status/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
            "sn": thermostat_sn,    
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
            // console.log("Thermostat status response for ", thermostat_sn, response.data)
            online = res;
            }
        } catch(error) {
                console.log(error)
        }
};
    
</script>

<div class="grid grid-cols-2 md:grid-cols-5 gap-2 max-w-screen-md">
    <div class="flex flex-row items-center">
        <div class="pr-3 cursor-pointer" title={status === true && online === true ? 'Call for heat' : 'Idle'}>
            <svg class="fill-current w-5" class:text-yellow-600={status === true && online === true} x="0px" y="0px" viewBox="0 0 60 60" style="enable-background:new 0 0 60 60;" xml:space="preserve"><path d="M29.107666,5c-3.1914063,0-5.7880859,2.5961914-5.7880859,5.7875977v21.8710938  c-3.8022461,2.1074219-6.1376953,6.0424805-6.1376953,10.4155273C17.1818848,49.6499023,22.5319824,55,29.107666,55  s11.9257813-5.3500977,11.9257813-11.9257813c0-4.3730469-2.3359375-8.3081055-6.1381836-10.4155273V10.7875977  C34.8952637,7.5961914,32.2990723,5,29.107666,5z M39.0334473,43.0742188C39.0334473,48.5473633,34.5808105,53,29.107666,53  s-9.9257813-4.4526367-9.9257813-9.9257813c0-3.8139648,2.137207-7.2285156,5.5771484-8.9111328  c0.3427734-0.1679688,0.5605469-0.5166016,0.5605469-0.8984375V10.7875977C25.3195801,8.6992188,27.0187988,7,29.107666,7  c2.0883789,0,3.7875977,1.6992188,3.7875977,3.7875977v22.4770508c0,0.3818359,0.2177734,0.7304688,0.5605469,0.8984375  C36.8962402,35.8457031,39.0334473,39.2602539,39.0334473,43.0742188z"></path><path d="M30.107666,15.3300781c0-0.5522461-0.4477539-1-1-1s-1,0.4477539-1,1v21.3045654  c-3.1233521,0.4837646-5.5244141,3.1828003-5.5244141,6.4395752c0,3.5976563,2.9267578,6.5244141,6.5244141,6.5244141  c3.597168,0,6.5239258-2.9267578,6.5239258-6.5244141c0-3.2567749-2.4009399-5.9558105-5.5239258-6.4395142V15.3300781z   M33.6315918,43.0742188c0,2.4946289-2.0292969,4.5244141-4.5239258,4.5244141s-4.5244141-2.0297852-4.5244141-4.5244141  s2.0297852-4.5244141,4.5244141-4.5244141S33.6315918,40.5795898,33.6315918,43.0742188z"></path><path d="M37.5217285,10.5600586h4.2963867c0.5522461,0,1-0.4477539,1-1s-0.4477539-1-1-1h-4.2963867c-0.5522461,0-1,0.4477539-1,1  S36.9694824,10.5600586,37.5217285,10.5600586z"></path><path d="M37.5217285,15.3476563h2.3320313c0.5522461,0,1-0.4477539,1-1s-0.4477539-1-1-1h-2.3320313c-0.5522461,0-1,0.4477539-1,1  S36.9694824,15.3476563,37.5217285,15.3476563z"></path><path d="M37.5217285,20.1357422h4.2963867c0.5522461,0,1-0.4477539,1-1s-0.4477539-1-1-1h-4.2963867c-0.5522461,0-1,0.4477539-1,1  S36.9694824,20.1357422,37.5217285,20.1357422z"></path><path d="M37.5217285,24.9233398h2.3320313c0.5522461,0,1-0.4477539,1-1s-0.4477539-1-1-1h-2.3320313c-0.5522461,0-1,0.4477539-1,1  S36.9694824,24.9233398,37.5217285,24.9233398z"></path><path d="M37.5217285,29.7109375h4.2963867c0.5522461,0,1-0.4477539,1-1s-0.4477539-1-1-1h-4.2963867c-0.5522461,0-1,0.4477539-1,1  S36.9694824,29.7109375,37.5217285,29.7109375z"></path></svg>        
        </div>
        <div>
            {room.room_type}
        </div>   
    </div>

    <div>
       Set to <span class="font-semibold">{room.thermostat.set_temperature}</span> °F
    </div>
    {#if room_temp && online}
    <div>
        (Current: <span class="font-semibold"> {room_temp || '--'} </span> °F) 
    </div>
    {:else}
    <div>
        (Current: -- °F) 
    </div>
    {/if}
    <div>
        {#if online}
        <div title="Device is online">
            <svg class="w-5 fill-current text-green-500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><g><path d="M85.2,37.2C47.9,3,15,37,14.7,37.3c-1.1,1.2-1.1,3.1,0.1,4.2c1.2,1.1,3.1,1.1,4.2-0.1c1.2-1.2,29.2-30,62.1,0.1   c0.6,0.5,1.3,0.8,2,0.8c0.8,0,1.6-0.3,2.2-1C86.5,40.2,86.4,38.3,85.2,37.2z"></path><path d="M25.5,47.2c-1.1,1.2-1.1,3.1,0.1,4.2c1.2,1.1,3.1,1.1,4.2-0.1c0.8-0.8,18.9-19.6,40.4,0.2c0.6,0.5,1.3,0.8,2,0.8   c0.8,0,1.6-0.3,2.2-1c1.1-1.2,1-3.1-0.2-4.2C48.5,23.4,25.7,46.9,25.5,47.2z"></path><path d="M34.9,57.3c-1.1,1.2-1.1,3.1,0.1,4.2c1.2,1.1,3.1,1.1,4.2-0.1C39.7,61,49.4,51,60.9,61.6c0.6,0.5,1.3,0.8,2,0.8   c0.8,0,1.6-0.3,2.2-1c1.1-1.2,1-3.1-0.2-4.2C49.1,42.7,35,57.2,34.9,57.3z"></path><path d="M50,66.3c-3.3,0-5.9,2.6-5.9,5.9s2.6,5.9,5.9,5.9c3.3,0,5.9-2.6,5.9-5.9S53.3,66.3,50,66.3z"></path></g></svg>
        </div>
        {:else}
        <div title="Device is offline">
            <svg class="w-5 fill-current text-gray-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g><path d="M50.048,61.368c4.418,0,8.421,1.798,11.323,4.699l4.691-4.691c-3.373-3.372-7.801-5.686-12.737-6.404l-6.799,6.8   C47.661,61.516,48.837,61.368,50.048,61.368z"></path><path d="M43.477,70.818l6.571,6.572l6.571-6.572c-1.681-1.683-4.006-2.723-6.571-2.722C47.482,68.097,45.158,69.136,43.477,70.818z   "></path><path d="M50.048,41.544c-9.882-0.001-18.845,4.02-25.336,10.51l4.693,4.691c3.758-3.757,8.535-6.491,13.872-7.764l7.421-7.422   C50.481,41.557,50.266,41.544,50.048,41.544z"></path><path d="M70.692,56.746l4.69-4.691c-3.255-3.255-7.133-5.888-11.435-7.705l-5.167,5.166C63.329,50.944,67.401,53.454,70.692,56.746   z"></path><path d="M50.048,28.319c-13.528,0-25.797,5.503-34.682,14.39l4.692,4.692c7.684-7.684,18.292-12.442,29.991-12.443   c2.286,0,4.527,0.187,6.717,0.537l5.605-5.606C58.432,28.865,54.303,28.319,50.048,28.319z"></path><path d="M68.905,39.392c4.137,2.062,7.897,4.771,11.134,8.006l4.69-4.691c-3.223-3.224-6.897-5.995-10.911-8.228L68.905,39.392z"></path></g><path d="M50.277,4.35C25.106,4.35,4.627,24.829,4.627,50c0,25.172,20.479,45.65,45.65,45.65c25.172,0,45.65-20.479,45.65-45.65  C95.928,24.829,75.449,4.35,50.277,4.35z M50.277,10.936c9.419,0,18.069,3.351,24.823,8.923L20.136,74.823  C14.564,68.069,11.213,59.419,11.213,50C11.213,28.46,28.738,10.936,50.277,10.936z M50.277,89.063  c-9.418,0-18.068-3.35-24.821-8.921L80.42,25.179c5.571,6.753,8.921,15.403,8.921,24.821C89.341,71.54,71.817,89.063,50.277,89.063z  "></path></svg>
        </div>
        {/if}
    </div>
</div>


