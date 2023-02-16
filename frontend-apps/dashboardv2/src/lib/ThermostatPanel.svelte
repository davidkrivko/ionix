<script>
    import axios from "axios";

    import ThermostatControls from "./ThermostatControls.svelte";
    import ThermostatItem from "./ThermostatItem.svelte";
    import { scale } from "svelte/transition";
    import { toast } from "@zerodevx/svelte-toast";
    import { getCsrfCookieValue } from "./utils";

    let selectedThermostat;
    const zoneNamesMap = new Object();

    async function getOwnThermostats() {
        const endpoint = "/api/devices/v2/thermostats/";

        try {
            const resp = await axios({
                method: "GET",
                url: endpoint,
            });
            if (resp.status === 200) {
                // console.log("Thersmostats", resp.data);
                const data = resp.data;
                const zonesThermostatsMap = new Object();
                for (const el of data) {
                    if (!zonesThermostatsMap[el.zone.id]) {
                        zonesThermostatsMap[el.zone.id] = new Array();
                    }
                    zonesThermostatsMap[el.zone.id].push(el);
                    zoneNamesMap[el.zone.id] = el.zone.name;
                }
                // console.log("zonesThermostatsMap", zonesThermostatsMap);
                return zonesThermostatsMap;
            }
        } catch (err) {
            console.log(err);
        }
    }

    async function updateZoneName(zoneId, name) {
        const endpoint = "/api/properties/zone/changename/";
        const csrfcookie = getCsrfCookieValue();
        try {
            const resp = await axios({
                method: "POST",
                url: endpoint,
                data: {
                    name: name,
                    id: zoneId,
                },
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (resp.status === 200) {
                toast.push("Zone name was successfully updated");
            }
        } catch (err) {
            console.log(err);
        }
    }

    function handleThermostatSelection(item) {
        selectedThermostat = item;
    }
</script>

<div class="flex flex-col gap-y-4">
    {#if !selectedThermostat}
        {#await getOwnThermostats() then zonesThermostatsMap}
            {#each Object.entries(zonesThermostatsMap) as [zoneId, thermostats]}
                <div class="py-2">
                    <div>
                        <input
                            value={zoneNamesMap[zoneId]}
                            on:change={(e) =>
                                updateZoneName(zoneId, e.target.value)}
                            class="input cursor-pointer input-ghost font-semibold focus:outline-none focus:shadow focus:cursor-text"
                        />
                    </div>
                    <div class="font-semibold" />
                    <div class="grid grid-cols-1 gap-y-2">
                        {#each thermostats as thermostat}
                            <ThermostatItem
                                {thermostat}
                                on:select={() =>
                                    handleThermostatSelection(thermostat)}
                            />
                        {/each}
                    </div>
                </div>
            {:else}
                <div class="text-sm">No configured devices to display</div>
            {/each}
        {/await}
    {:else}
        <div in:scale class="flex flex-col gap-y-6 shadow-md p-6 rounded-md">
            <ThermostatControls
                thermostat={selectedThermostat}
                on:close={() => (selectedThermostat = undefined)}
            />
        </div>
    {/if}
</div>
