<script>
    export let thermostat;
    import axios from "axios";
    import { formatTimeAgo, determiteOnlineStatus } from "./utils";

    import { createEventDispatcher, onMount } from "svelte";
    const dispatch = createEventDispatcher();

    let onlineStatus;
    let lastReadingAgo;
    let sensorTemp;

    onMount(() => {
        getPersontalThermostatData();
    });

    async function getPersontalThermostatData() {
        const endpoint = `/api/devices/v2/thermostat/data/${thermostat.serial_num}/`;
        try {
            const resp = await axios({
                method: "GET",
                url: endpoint,
            });
            if (resp.status === 200) {
                sensorTemp = resp.data?.t1;
                lastReadingAgo = formatTimeAgo(new Date(resp.data?.timestamp));
                onlineStatus = determiteOnlineStatus(resp.data.timestamp);
            }
        } catch (err) {
            console.log(err);
        }
    }

    function formatThermostatName() {
        if (thermostat.name.length === 0) {
            return thermostat.serial_num;
        } else return thermostat.name.slice(0, 20);
    }

    function formatThermostatTemp() {
        if (onlineStatus) return `${sensorTemp}°F`;
        else return "--";
    }
</script>

<div>
    <button
        on:click={() => dispatch("select")}
        class="btn btn-wide btn-sm btn-outline flex flex-row justify-evenly"
    >
        <span>{formatThermostatName()}</span>
        {#key onlineStatus}
            <span>{formatThermostatTemp()}</span>
        {/key}
    </button>
</div>
