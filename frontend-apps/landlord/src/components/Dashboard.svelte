<script>
import Sidebar from './shared/Sidebar.svelte';
import Footer from './shared/Footer.svelte';
import Profile from './Profile.svelte';
import Settings from './Settings.svelte';
import Messenger from './shared/Messenger.svelte';
import Support from './Support.svelte';
import Properties from './Properties.svelte';
import Apartments from './Apartments.svelte';
import Stats from './Stats.svelte';

import { 
  selected_dashboard_component, 
  messenger,
} from '../stores/store';



const options = [
  { name: 'properties', 'component': Properties },
  { name: 'apartments', 'component': Apartments },
  // { name: 'tenants', 'component': Tenants },
  { name: 'settings', 'component': Settings },
  { name: 'profile', 'component': Profile },
  { name: 'support', 'component': Support },
  { name: 'stats', 'component': Stats },
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
    <title>Landlord dashboard – IoniqBox</title>
</svelte:head>

{#if $messenger}
  <Messenger />
{/if}
<div class="w-full rounded-3xl mx-auto ts-bg p-2 bg-white bg-opacity-25 shadow-md max-w-screen-xl">
  <div class="flex flex-row bg-white rounded-2xl pl-1 md:pl-3">
    <div>
      <Sidebar />
    </div>

      <div class="flex flex-col flex-grow w-full">
              <svelte:component this={selected.component} />
      <!-- <Footer /> -->
      </div>
      
  </div>
</div>