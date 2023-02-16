<script>
    export let controllerSerial;

    import axios from "axios";
    import { createEventDispatcher, onMount } from "svelte";
    import { determiteOnlineStatus } from "./utils";

    const dispatch = createEventDispatcher();
    let onlineStatus;
    // let lastReadingAgo;
    let t1;
    let t2;

    onMount(() => {
        getControllerDataFromStream();
    });

    async function getControllerDataFromStream() {
        const endpoint = `/api/devices/v2/controller/data/${controllerSerial}/`;
        try {
            const resp = await axios({
                method: "GET",
                url: endpoint,
            });
            if (resp.status === 200) {
                // console.log("Controller stream data", resp.data);
                t1 = resp.data?.t1;
                t2 = resp.data?.t2;
                // lastReadingAgo = formatTimeAgo(new Date(resp.data?.timestamp));
                onlineStatus = determiteOnlineStatus(resp.data.timestamp)
                    ? "online"
                    : "offline";
            }
        } catch (err) {
            console.log(err);
        }
    }
</script>

<!-- <div class="flex flex-row items-center gap-x-3">
    <div class="text-sm">IONIQ Thermostat</div>
    <div>online</div>
    <input
        bind:value={thermostat.name}
        on:change={() => changeThermostatName()}
        class="input input-sm cursor-pointer input-ghost font-semibold focus:outline-none focus:shadow focus:cursor-text"
    />
</div> -->

<div class="flex flex-row items-center gap-x-3">
    <div class="text-sm">IONIQ Controller</div>
    <!-- <div>online</div> -->
    <input
        value={controllerSerial}
        disabled
        class="input input-sm cursor-pointer input-ghost font-semibold focus:outline-none focus:shadow focus:cursor-text"
    />
</div>

<div class="grid grid-cols-2 gap-x-2 gap-y-2 py-5 text-sm">
    <div>T1:</div>
    <div>
        {t1 || "--"}&deg;
    </div>
    <div>T2:</div>
    <div>
        {t2 || "--"}&deg;
    </div>
    <div>Status:</div>
    <div>
        {onlineStatus || "--"}
    </div>
</div>

<div class="pt-4 flex flex-row gap-x-5 items-center w-full justify-center">
    <button on:click={() => dispatch("close")} class="btn btn-outline btn-xs">
        Back
    </button>
</div>
