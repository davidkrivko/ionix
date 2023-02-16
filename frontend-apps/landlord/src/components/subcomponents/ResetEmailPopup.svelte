<script>
export let tenant;

import { createEventDispatcher } from 'svelte';
import { fade } from 'svelte/transition';

const dispatch = createEventDispatcher();

let email = tenant?.email;

</script>


<div in:fade class="place-items-center absolute z-50 bg-white shadow-2xl">
    <div class="p-5 max-w-md">
       <h3 class="text-center font-bold text-lg">Please, review the email</h3>
       <div class="py-4 flex flex-row justify-center">
            <input type="email" bind:value={email} class="px-2 py-1 ring-1 ring-gray-500 text-center">
       </div>
       <div>
        We're going to send an access link to the user email above. You can change it or proceed with current one.
       </div>
        <div class="grid grid-cols-2 gap-x-1 py-2">
            <button on:click={() => dispatch('confirm', email)} class="ring-green-400 ring-2 py-2 px-4 mr-5">Next</button>
            <button on:click|stopPropagation={() => dispatch('cancel')} class="ring-red-400 ring-2 py-2 px-4">Cancel</button>
        </div>
    </div>
</div>