
<script>
import axios from "axios";
import { onMount } from 'svelte';
import { fade } from 'svelte/transition';
import { boiler_id, outdoor_temp } from '../../stores/store';
import { getCsrfCookieValue, fetchIoniqOnlineStatus } from '../../lib/utils';
// let shutdown_active = false;
// let shutdown_enabled = false;

let endswitch;
let online_status;

onMount(() => {
    getZipTemperature();
    
    setTimeout(() => getEndSwitchStatus(), 3000);
    // fetchBoilerData();

    // const boilerdata_interval = setInterval(()=> fetchBoilerData(), 5000);
    const weatherdata_interval = setInterval(() => getZipTemperature(), 30000);
    const controllerdata_interval = setInterval(()=> getEndSwitchStatus(), 20000);

    return () => {
        // clearInterval(boilerdata_interval);
        clearInterval(weatherdata_interval);
        clearInterval(controllerdata_interval);
    }
})

async function getZipTemperature() {
    try {
    const endpoint = '/api/properties/gettemp/';
  
    const response = await axios({
        url: endpoint,
        method: "get",
     });
    if(response.status === 200) {
            $outdoor_temp = response.data.data.temp_f;
        }
    } catch(error) {
            console.log(error)
    }
};

async function getEndSwitchStatus() {

    const endpoint = `/api/devices/boiler/iodata/`;
    if ($boiler_id !== undefined) {
        try {
        const csrfcookie = getCsrfCookieValue();
        const data = {
            "id": $boiler_id
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
                endswitch = res.data?.endswitch;
                const controller_sn = res.data.controller;
                online_status = await fetchIoniqOnlineStatus(controller_sn);
            }
        } catch(error) {
                console.log(error)
        }
    }
};

// async function fetchBoilerData() {
//     if ($boiler_id !== undefined) {
//         try {
//         const endpoint = `/api/devices/boiler/status/${$boiler_id}/`;
    
//         const response = await axios({
//             url: endpoint,
//             method: "get",
//         });
//         if(response.status === 200) {
//                 shutdown_active = response.data.shutdown_active;
//                 shutdown_enabled = response.data.shutdown_enabled;
//             }
//         } catch(error) {
//                 console.log(error)
//         }
//     }
// };
</script>


<div class="w-full">
    <div class="card p-1 text-center mx-auto max-w-xs">
        <div class="card-body flex flex-col items-center justify-center p-2 rounded-md text-gray-700">
            <div class="flex flex-row items-center gap-x-4 py-0.5">
                <div class="font-semibold text-lg">Outdoor:</div>
                <div class="font-bold text-2xl">
                    {$outdoor_temp || '--'} °
                </div>
            </div>
            {#if online_status === false}
            <div in:fade title="Controller is offline">
                <svg class="w-5 fill-current text-gray-500" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g><path d="M50.048,61.368c4.418,0,8.421,1.798,11.323,4.699l4.691-4.691c-3.373-3.372-7.801-5.686-12.737-6.404l-6.799,6.8   C47.661,61.516,48.837,61.368,50.048,61.368z"></path><path d="M43.477,70.818l6.571,6.572l6.571-6.572c-1.681-1.683-4.006-2.723-6.571-2.722C47.482,68.097,45.158,69.136,43.477,70.818z   "></path><path d="M50.048,41.544c-9.882-0.001-18.845,4.02-25.336,10.51l4.693,4.691c3.758-3.757,8.535-6.491,13.872-7.764l7.421-7.422   C50.481,41.557,50.266,41.544,50.048,41.544z"></path><path d="M70.692,56.746l4.69-4.691c-3.255-3.255-7.133-5.888-11.435-7.705l-5.167,5.166C63.329,50.944,67.401,53.454,70.692,56.746   z"></path><path d="M50.048,28.319c-13.528,0-25.797,5.503-34.682,14.39l4.692,4.692c7.684-7.684,18.292-12.442,29.991-12.443   c2.286,0,4.527,0.187,6.717,0.537l5.605-5.606C58.432,28.865,54.303,28.319,50.048,28.319z"></path><path d="M68.905,39.392c4.137,2.062,7.897,4.771,11.134,8.006l4.69-4.691c-3.223-3.224-6.897-5.995-10.911-8.228L68.905,39.392z"></path></g><path d="M50.277,4.35C25.106,4.35,4.627,24.829,4.627,50c0,25.172,20.479,45.65,45.65,45.65c25.172,0,45.65-20.479,45.65-45.65  C95.928,24.829,75.449,4.35,50.277,4.35z M50.277,10.936c9.419,0,18.069,3.351,24.823,8.923L20.136,74.823  C14.564,68.069,11.213,59.419,11.213,50C11.213,28.46,28.738,10.936,50.277,10.936z M50.277,89.063  c-9.418,0-18.068-3.35-24.821-8.921L80.42,25.179c5.571,6.753,8.921,15.403,8.921,24.821C89.341,71.54,71.817,89.063,50.277,89.063z  "></path></svg>
            </div>
            {:else if endswitch === 1 }
            <div in:fade title="Active">
                <svg class="w-4 fill-current text-yellow-600" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                    <g>
                    <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                    </path>
                    </g>
                </svg>
            </div>
            {:else if endswitch === 0 }
            <div in:fade title="Standby">
                <svg class="w-4 fill-current text-gray-400" version="1.1" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;" viewBox="0 0 333 333" x="0px" y="0px" fill-rule="evenodd" clip-rule="evenodd">
                    <g>
                    <path d="M53 288l227 0 0 37 -227 0 0 -37zm106 -279c17,-5 42,18 55,40 116,180 -118,130 -40,228 -17,5 -42,-18 -55,-40 -115,-179 117,-132 40,-228z">
                    </path>
                    </g>
                </svg>
            </div>
            {/if}
            <!-- {#if shutdown_enabled}
            <div in:fade class="flex flex-row gap-x-4">
                <div class="w-6 cursor-pointer" title="You've enabled warm weather boiler shutdown mode">
                    <svg class="fill-current text-gray-400" class:text-green-500={shutdown_active} xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path fill-rule="evenodd" clip-rule="evenodd" d="M81.8007813,18.1748047C90.6005859,26.9755859,95,37.5751953,95,49.9755859  c0,12.4335938-4.3994141,23.0332031-13.1992188,31.7998047C73.0332031,90.5751953,62.4335938,94.9755859,50,94.9755859  c-12.4326172,0-23.0498047-4.4003906-31.8496094-13.2001953C9.3837891,73.0087891,5,62.4091797,5,49.9755859  c0-12.4003906,4.3837891-23,13.1503906-31.8007813C26.9501953,9.4091797,37.5673828,5.0253906,50,5.0253906  C62.4335938,5.0253906,73.0332031,9.4091797,81.8007813,18.1748047z M19.3505859,62.0751953  c0.0664063-0.0664063,0.1494141-0.1171875,0.25-0.1503906c26.6669922,20.8007813,49.5332031,12.5839844,68.5996094-24.6494141  c-38.3994141-17.9667969-61.25-12.4501953-68.5498047,16.5498047c7.7666016-3.9003906,17.0166016-5.8339844,27.75-5.7998047  C36.5,49.6591797,26.9501953,52.9755859,18.75,57.9755859c-0.4667969,0.265625-0.9492188,0.5664063-1.4492188,0.8994141  C17.2001953,58.9423828,17.1005859,59.0087891,17,59.0751953c-1.5332031,0.9667969-3.0166016,2.0166016-4.4492188,3.1503906  c-0.4003906,0.2998047-0.6337891,0.6992188-0.7001953,1.1992188C11.75,63.9580078,11.8837891,64.4423828,12.25,64.875  c0.3007813,0.4003906,0.7001953,0.6337891,1.2001953,0.7001953s0.9833984-0.0664063,1.4501953-0.4003906  c1.3330078-1.0332031,2.7167969-2.015625,4.1503906-2.9492188C19.1835938,62.1923828,19.2832031,62.1416016,19.3505859,62.0751953z"></path></svg>
                </div>
                {#if shutdown_active}
                <div class="w-6 cursor-pointer" title="Warm weather shutdown mode turned off the heating">
                    <svg class="fill-current text-red-500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><g><path d="M81.042,17.467c-0.021-0.024-0.029-0.055-0.051-0.077c-0.029-0.029-0.067-0.039-0.098-0.065C72.826,9.694,61.954,5,50,5   C25.187,5,5,25.187,5,50c0,11.925,4.671,22.773,12.269,30.834c0.041,0.054,0.062,0.118,0.111,0.167   c0.039,0.039,0.09,0.054,0.132,0.088C25.709,89.651,37.238,95,50,95c24.813,0,45-20.187,45-45   C95,37.215,89.632,25.667,81.042,17.467z M50,8c10.629,0,20.342,3.977,27.748,10.51L58.8,37.459   c-2.14-4.226-3.354-8.878-2.925-13.664c0.055-0.617,1.191-5.548-0.725-3.915c-8.001,6.82-15.122,14.911-21.053,23.583   c-2.076,3.035-4.036,6.385-5.362,9.863c-1.834,4.812-2.445,9.868-0.477,14.677l-9.746,9.746C11.977,70.343,8,60.63,8,50   C8,26.841,26.841,8,50,8z M48.819,47.44l-9.594,9.595c1.929-4.286,5.305-7.931,8.493-11.287c0.31-0.326,0.853-0.134,0.898,0.313   C48.661,46.506,48.741,46.992,48.819,47.44z M50,92c-11.452,0-21.844-4.612-29.428-12.07l9.143-9.143   c0.186,0.288,0.373,0.576,0.581,0.861c3.42,4.695,8.205,6.572,13.352,8.465c0.574,0.211,1.857,0.616,2.08,0.046   c0.182-0.465-0.29-0.906-0.694-1.199c-4.955-3.604-7.839-10.032-7.338-16.153l11.533-11.533c0.083,0.998,0.181,1.994,0.316,2.987   c0.486,3.567,1.388,7.172,3.458,10.174c1.529,2.217,2.337-2.421,2.714-3.368c0.788-1.98,1.739-3.894,2.833-5.723   c0.243-0.406,3.73,5.618,3.923,6.267c0.701,2.366,0.792,4.89,0.426,7.322c-0.361,2.394-1.78,7.513-4.023,10.24   c-0.337,0.41,0.07,0.992,0.573,0.823c0.549-0.185,1.044-0.346,1.543-0.644c2.65-1.583,5.51-3.767,7.416-6.174   c1.926-2.433,3.346-4.816,4.148-7.828c0.995-3.733,0.079-8.042-1.695-11.484c-2.645-5.131-7.47-8.794-10.539-13.686l19.608-19.608   C87.388,28.156,92,38.548,92,50C92,73.159,73.159,92,50,92z"></path></g></svg>
                </div>
                {/if}
            </div>
            {/if} -->
        </div>
    </div>
</div>


<style>
    .card {
    /* word-wrap: break-word; */
    max-width: 180px;
    background-color: #e6e7ee;
    background-clip: border-box;
    border: 0.0625rem solid rgba(243,247,250,.05);
    border-radius: 0.55rem;
    }
    .card-body {
        box-shadow: 6px 6px 12px #b8b9be,-6px -6px 12px #fff!important;
    }

</style>