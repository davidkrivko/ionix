<script>
export let controller_sn;
import {fade, scale} from 'svelte/transition';
import ApexCharts from 'apexcharts';
import { onMount } from 'svelte';
import axios from 'axios';
import { getCsrfCookieValue } from '../../lib/utils';
import DatePicker from "@beyonk/svelte-datepicker/src/components/DatePicker.svelte";

import { createEventDispatcher } from 'svelte';

let chartdiv;
let loader = false;
let graph = false;
let start_date = new Date();
let start_date_picker = false;
let end_date = new Date();
let end_date_picker = false;

const dispatch = createEventDispatcher();

onMount(() => {
    console.log("controller_sn", controller_sn)
    // fetchData();

});


async function fetchData(){
    loader = true;
    const endpoint = '/api/visuals/heatcycles/';
    try {
    const csrfcookie = getCsrfCookieValue();
    const payload = {
        'sn': controller_sn,
        'start_date': start_date.toISOString().substring(0,10),
        'end_date': end_date.toISOString().substring(0,10),
    }
    console.log("payload", payload)
    const response = await axios({
        url: endpoint,
        method: "post",
        data: payload,
        headers: {
            'X-CSRFToken': csrfcookie
        }

    });
    if(response.status === 200) {
        console.log("response", response);
        loader = false;
        graph = true;
        renderChart(response.data.data)
            // $message = "Heating settings were successfully updated"
            // $messenger = true;
            // dispatch('change');
        }
    } catch(error) {
            console.log(error)
    }
}

const data = [];

function renderChart(data) {

    const options = {
        series: [{
            name: 'Heating cycles',
            type: 'column',
            data: data?.date_cycles_count
        }, {
        name: 'Outdoor temp',
            type: 'line',
            data: data.date_temp_list_f,
        }],
            chart: {
            height: 350,
            type: 'line',
        },
        stroke: {
            width: [0, 4]
        },
        title: {
            text: 'Boiler data - Heating cycles by day'
        },
        dataLabels: {
            enabled: true,
            enabledOnSeries: [1]
        },
        labels: data.date_labels,
        xaxis: {
            type: 'datetime'
        },
        yaxis: [{
            title: {
            text: 'Number of cycles',
            },
        
        }, {
            opposite: true,
            title: {
            text: 'Temperature in F'
            }
        }]
};

const chart = new ApexCharts(chartdiv, options);
chart.render();
};

function handleStartDateSelect(e) {
    console.log(e)
    start_date = e.detail.date;
};

function handleEndDateSelect(e) {
    end_date = e.detail.date;
}

</script>

<div class="px-4">
    <h1 class="py-2 text-sm">
        Heating cycles
    </h1>
    <div class="flex flex-row gap-5 flex-wrap">
        <div class="text-sm">
            <DatePicker on:date-selected={handleStartDateSelect} placeholder="Choose start date"/>
        </div>
        <div class="text-sm">
            <DatePicker on:date-selected={handleEndDateSelect} placeholder="Choose end date" />
        </div>
        <div>
            <button on:click={() => fetchData()} class="px-4 py-2 ring-1 text-sm">Load data</button>
        </div>
    </div>

    {#if loader}
    <div in:fade class="flex flex-col items-center">
        <div class="py-2 text-xs">
            Loading data...
        </div>
        <img src="/static/loader.svg" alt="loader">
    </div>
    {/if}
    <div bind:this={chartdiv} class="py-3">
    </div>
</div>


