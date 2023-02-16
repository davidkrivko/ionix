<script>
    import QRious from 'qrious';
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { qcodepopup } from '../../stores/store';

    export let link;
    let canvas;

    onMount(() => {
        const qrCode = new QRious({
            element: canvas,
            value: link,
            size: 220,
        });
    })

</script>



<div in:fade class="absolute left-0 top-0 w-full h-full justify-center items-center z-20 bg-white cursor-pointer bg-opacity-70" on:click|self={() => $qcodepopup = false} >

    <div class="flex flex-row mt-20 justify-center items-center">
       <div><canvas bind:this={canvas}></canvas></div>
    </div>

</div>