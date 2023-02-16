<script>
export let note = '';
// export const id = undefined;

import { fade } from 'svelte/transition'
import { createEventDispatcher } from  'svelte'

const dispatch = createEventDispatcher();

</script>


<div in:fade class="place-items-center absolute z-50 bg-white shadow-2xl">
    <div class="p-5 max-w-md">
       <h3 class="text-center font-bold text-lg">Are you sure?</h3>
        <div class="text-sm py-4">
            {note}
        </div>
        <div class="grid grid-cols-2 gap-x-1 py-2">
            <button on:click={() => dispatch('confirm')} class="ring-green-400 ring-2 py-2 px-4 mr-5">Yes</button>
            <button on:click|stopPropagation={() => dispatch('cancel')} class="ring-red-200 ring-2 py-2 px-4">No</button>
        </div>
    </div>
</div>