<script>
    import { fade } from 'svelte/transition'
    import { createEventDispatcher } from 'svelte';
    export let content;

    const dispatch = createEventDispatcher();


</script>


<div in:fade class="absolute p-5 -left-2 bg-white shadow-md rounded-lg w-52 z-30">
    <div class="absolute top-1 right-1 z-40">
        <button on:click={()=> dispatch('close')}>
            <svg class="w-5 text-gray-700 fill-current" viewBox="0 0 48 48" x="0px" y="0px"><g data-name="Application, Close"><path d="M25.41,24l11.3,11.29-1.42,1.42L24,25.41,12.71,36.71l-1.42-1.42L22.59,24,11.29,12.71l1.42-1.42L24,22.59l11.29-11.3,1.42,1.42Z"></path></g></svg>
        </button>
    </div>
    <div class="font-semibold mx-auto">
        {content}
    </div>

</div>