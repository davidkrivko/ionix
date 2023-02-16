<script>
import axios from 'axios';
import { onMount } from 'svelte';
import { fade } from 'svelte/transition';

import Header from './shared/Header.svelte';
import Sidebar from './shared/Sidebar.svelte';
import MobileMenu from './shared/MobileMenu.svelte';
import Footer from './shared/Footer.svelte';
import Rooms from './Rooms.svelte';
import Profile from './Profile.svelte';
import PlaceHolder from './PlaceHolder.svelte';
import Access from './Access.svelte';
import Settings from './Settings.svelte';
import Messenger from './shared/Messenger.svelte';
import Support from './Support.svelte';

import { 
  selected_dashboard_component, 
  mobile_menu,
  messenger,
} from '../stores/store';


const options = [
  { name: 'rooms', 'component': Rooms },
  { name: 'profile', 'component': Profile },
  { name: 'access', 'component': Access },
  { name: 'settings', 'component': Settings },
  { name: 'stats', 'component': PlaceHolder },
  { name: 'support', 'component': Support },
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
    <title>Owner dashboard – IoniqBox</title>
</svelte:head>



        {#if $messenger}
          <Messenger />
        {/if}
        <div class="flex flex-row flex-grow py-6">

            <div class="hidden md:block">
                <Sidebar />
            </div>
            
            <div class="flex flex-col flex-grow w-full">
                <div class="flex flex-col flex-grow w-full px-4 md:px-6">
                    <svelte:component this={selected.component} />
                </div>
                <Footer />
            </div>

        </div>


<style>

</style>