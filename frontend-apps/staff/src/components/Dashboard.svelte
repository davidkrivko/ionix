<script>
import axios from 'axios';
import { onMount } from 'svelte';
import { fade } from 'svelte/transition';

import Header from './shared/Header.svelte';
import Sidebar from './shared/Sidebar.svelte';
import MobileMenu from './shared/MobileMenu.svelte';
import Footer from './shared/Footer.svelte';
import Messenger from './shared/Messenger.svelte';
import Placeholder from './Placeholder.svelte';
import Controllers from './Controllers.svelte';
import Thermostats from './Thermostats.svelte';


import { 
  selected_dashboard_component, 
  mobile_menu,
  messenger,
} from  '../stores/store';


const options = [
  { name: 'controllers', 'component': Controllers },
  { name: 'thermostats', 'component': Thermostats },
  // { name: 'stats', 'component': Placeholder },
];

let selected = options[0];


function evalSelected() {
	for (const [i, v] of options.entries()) {
		if (v.name === $selected_dashboard_component) {
		selected = options[i]
		}
	}
}

$: evalSelected(), $selected_dashboard_component;
</script>

<svelte:head>
    <title>Staff dashboard – IoniqBox</title>
</svelte:head>

        <Header />
            {#if $mobile_menu}
                <MobileMenu />
            {/if}

        {#if $messenger}
          <Messenger />
        {/if}
        <div class="flex flex-row flex-grow py-6">

            <div class="hidden md:block">
                <Sidebar />
            </div>
            
            <div class="flex flex-col flex-grow max-w-screen-xl">
                <div class="flex flex-col flex-grow px-4 md:px-6">
                    <svelte:component this={selected.component} />
                </div>

                <Footer />
            </div>

        </div>


<style>

</style>