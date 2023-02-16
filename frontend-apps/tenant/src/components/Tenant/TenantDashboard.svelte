<script>
import { fade } from 'svelte/transition';

import Header from '../shared/Header.svelte';
import Rooms from './Rooms.svelte';
import Footer from '../shared/Footer.svelte';
import Profile from './Profile.svelte';

import { selected_component } from '../../stores/store';

const options = [
  { name: 'rooms', 'component': Rooms },
  { name: 'profile', 'component': Profile },
];

let selected = options[0];


function evalSelected() {
	for (const [i, v] of options.entries()) {
		if (v.name === $selected_component) {
		selected = options[i]
		}
	}
}

$: evalSelected(), $selected_component;
</script>

<svelte:head>
    <title>Tenant dashboard</title>
</svelte:head>

        <Header />
            <div in:fade class="mx-auto flex-grow max-w-screen-lg py-6">
                <svelte:component this={selected.component} />
            </div>
        <Footer />

<style>

</style>