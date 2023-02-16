<script>
  import { SvelteToast } from "@zerodevx/svelte-toast";
  import { selected_component } from "./lib/store";

  import ThermostatPanel from "./lib/ThermostatPanel.svelte";
  import Profile from "./lib/Profile.svelte";

  const toastOptions = {
    duration: 3000, // duration of progress bar tween to the `next` value
    initial: 1, // initial progress bar value
    next: 0, // next progress value
    pausable: true, // pause progress bar tween on mouse hover
    dismissable: true, // allow dismiss with close button
    reversed: false, // insert new toast to bottom of stack
    intro: { x: 256 }, // toast intro fly animation settings
  };

  const components = [ThermostatPanel, Profile];
</script>

<svelte:head>
  <title>Ioniqbox - Devices</title>
</svelte:head>

<main class="flex flex-col min-h-screen">
  <div
    class="flex flex-row gap-x-4 items-center w-full h-20 bg-black text-white px-6 py-2 relative"
  >
    <div class="flex-grow text-lg font-semibold">
      <button on:click={() => ($selected_component = 0)}>IONIQBOX</button>
    </div>
    <div class="flex flex-row gap-x-2 text-sm" />
    <div>
      <div class="dropdown dropdown-bottom dropdown-end">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label tabindex="0" class="btn m-1">Account</label>
        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
        <ul
          tabindex="0"
          class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52 text-sm text-black"
        >
          <li>
            <button on:click={() => ($selected_component = 1)}>Profile</button>
          </li>
          <li>
            <a href="/logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="flex flex-grow justify-center items-center py-20">
    <svelte:component this={components[$selected_component]} />
  </div>
  <footer class="bg-black text-white px-6 py-4 h-12 text-sm">
    <span>&copy; IONIQBOX {new Date().getFullYear()}</span> -
    <span>support@turnonheat.com</span>
  </footer>
</main>

<SvelteToast options={toastOptions} />
