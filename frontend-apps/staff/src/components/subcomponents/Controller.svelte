<script>

export let controller;
import axios from 'axios';
import { onMount } from 'svelte';
import { getCsrfCookieValue } from '../../lib/utils';

let online = false;

onMount(()=> {
    getThermostatData();
    const status_update_interval = setInterval(()=> getThermostatData(), 30000);

    return ()=> clearInterval(status_update_interval);
})


async function getThermostatData() {
  
  const endpoint = `/api/devices/status/`;
    try {
    const csrfcookie = getCsrfCookieValue();
    const data = {
      "sn": controller.serial_num
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
        const status_timestamp = new Date(response.data.realtime)
            if (typeof status_timestamp !== undefined) {
                const now = new Date()
                // @ts-ignore
                const timedelta_sec = parseInt((now - status_timestamp)/1000);
                timedelta_sec <= 10 ? online = true : online = false;
            }
        }
    } catch(error) {
        console.log(error)
    }
};
</script>


<div>
    {controller.serial_num}
</div>
<div class="hidden md:block">
    {controller.owner}
</div>
<div>
    {controller.model_type === 'MX' ? 'Max' : 'Mini'}
</div>
<div class="cursor-pointer flex flex-row justify-center items-center" title="Online status">
    <svg class="fill-current w-4 text-gray-500" class:text-green-400={online} version="1.1" x="0px" y="0px" viewBox="0 0 100 100">
        <g transform="translate(0,-952.36218)">
            <path d="m 50.000001,959.36215 c -23.7482,0 -42.9999995,19.25188 -42.9999995,42.99995 0,23.7482 19.2517995,43.0001 42.9999995,43.0001 23.748201,0 42.999998,-19.2519 42.999998,-43.0001 0,-23.74807 -19.251797,-42.99995 -42.999998,-42.99995 z" stroke="none" marker="none" visibility="visible" display="inline" overflow="visible">
            </path>
        </g>
    </svg>
</div>