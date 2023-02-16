<script>
    export let thermostat;

    import axios from "axios";
    import { createEventDispatcher, onMount } from "svelte";
    import {
        getCsrfCookieValue,
        // formatTimeAgo,
        determiteOnlineStatus,
    } from "./utils";
    import { toast } from "@zerodevx/svelte-toast";
    import PopupWrapper from "./PopupWrapper.svelte";
    import ControllerData from "./ControllerData.svelte";
    import Schedule from "./Schedule.svelte";

    onMount(() => {
        if (thermostat.name.length === 0) {
            thermostat.name = thermostat.serial_num;
        }

        getPersontalThermostatData();
    });
    // console.log("Thermostat", thermostat);
    const dispatch = createEventDispatcher();

    let setpoint = thermostat.set_temperature;
    let controllerSerial;
    let onlineStatus;
    // let lastReadingAgo;
    let sensorTemp;
    let controllerDataView = false;
    let scheduleView = false;

    async function getPersontalThermostatData() {
        const endpoint = `/api/devices/v2/thermostat/data/${thermostat.serial_num}/`;
        try {
            const resp = await axios({
                method: "GET",
                url: endpoint,
            });
            if (resp.status === 200) {
                // console.log("Thermostat stream data", resp.data);
                controllerSerial = resp.data?.sn2;
                sensorTemp = resp.data?.t1;
                // lastReadingAgo = formatTimeAgo(new Date(resp.data?.timestamp));
                onlineStatus = determiteOnlineStatus(resp.data.timestamp)
                    ? "online"
                    : "offline";
            }
        } catch (err) {
            console.log(err);
        }
    }

    async function updatePersonalThermostatSetpoint() {
        const endpoint = "/api/devices/thermostat/set/";
        const csrfcookie = getCsrfCookieValue();
        try {
            const resp = await axios({
                method: "POST",
                url: endpoint,
                data: {
                    thermostat_sn: thermostat.serial_num,
                    set_temperature: setpoint,
                },
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (resp.status === 200) {
                console.log("Updated");
                toast.push("Setpoint was successfully set");
            }
        } catch (err) {
            console.log(err);
        }
    }

    async function changeThermostatName() {
        const endpoint = `/api/devices/thermostat/update/${thermostat.id}/`;
        const csrfcookie = getCsrfCookieValue();
        try {
            const resp = await axios({
                method: "POST",
                url: endpoint,
                data: {
                    name: thermostat.name,
                },
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (resp.status === 200) {
                // console.log("Updated");
                toast.push("Thermostat tag was successfully updated");
            }
        } catch (err) {
            console.log(err);
        }
    }
</script>

<div class="flex flex-row items-center gap-x-3">
    <div class="text-sm">IONIQ Thermostat</div>
    <!-- <div>online</div> -->
    <input
        bind:value={thermostat.name}
        on:change={() => changeThermostatName()}
        class="input input-sm cursor-pointer input-ghost font-semibold focus:outline-none focus:shadow focus:cursor-text"
    />
</div>

<div class="grid grid-cols-2 gap-x-2">
    <div>Setpoint</div>
    <div>
        {setpoint}&deg;
    </div>
</div>
<div>
    <input
        bind:value={setpoint}
        type="range"
        min="45"
        max="90"
        class="range range-sm range-primary"
    />
    <div class="w-full flex justify-between text-xs px-2">
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
        <span>|</span>
    </div>
</div>
<div class="grid grid-cols-2 gap-x-2 test-sm gap-y-3 items-center">
    <div>Linked controller:</div>
    <div>
        <button
            on:click={() =>
                controllerSerial ? (controllerDataView = true) : {}}
            class="btn btn-outline btn-sm">{controllerSerial || "--"}</button
        >
    </div>
    <div>Sensor temp:</div>
    <div>
        {sensorTemp || "--"}&deg;
    </div>
    <!-- <div>Last reading:</div> -->
    <!-- <div>
        {lastReadingAgo || "--"}
    </div> -->
    <div>Status:</div>
    <div>
        {onlineStatus || "--"}
    </div>
    <div>Schedule:</div>
    <div>
        <button
            class="btn-sm btn btn-outline"
            on:click={() => (scheduleView = true)}
        >
            Settings
        </button>
    </div>
</div>

<div class="py-4 flex flex-row gap-x-5 items-center w-full justify-center">
    <button
        on:click={updatePersonalThermostatSetpoint}
        class="btn btn-xs btn-primary"
    >
        Save
    </button>
    <button on:click={() => dispatch("close")} class="btn btn-outline btn-xs">
        Back
    </button>
</div>

{#if controllerDataView}
    <PopupWrapper on:close={() => (controllerDataView = false)}>
        <ControllerData
            bind:controllerSerial
            on:close={() => (controllerDataView = false)}
        />
    </PopupWrapper>
{/if}

{#if scheduleView}
    <PopupWrapper on:close={() => (scheduleView = false)}>
        <Schedule {thermostat} on:close={() => (scheduleView = false)} />
    </PopupWrapper>
{/if}
