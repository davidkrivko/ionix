<script>
export let active;

import { fade } from 'svelte/transition'
import { createEventDispatcher } from  'svelte'

const dispatch = createEventDispatcher();

</script>


{#if active}

<div in:fade class="place-items-center absolute z-50 bg-white shadow-2xl">
    <div class="p-5">
       <h3 class="text-center font-bold text-lg">Are you sure?</h3>

        <div class="flex flex-row mt-4">
            <button on:click={() => {dispatch('confirm'); active=false}} class="btn rounded ring-green-400 ring-2 py-2 px-4 mr-5">Yes</button>
            <button on:click|stopPropagation={() => {dispatch('cancel'); active = false}} class="btn btn-secondary py-2 px-4 mx-auto">No</button>
        </div>
    </div>
</div>
{/if}