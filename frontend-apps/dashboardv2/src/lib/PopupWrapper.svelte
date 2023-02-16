<script>
    import { createEventDispatcher } from "svelte";
    import { scale } from "svelte/transition";
    const dispatch = createEventDispatcher();
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div
    on:click|self={() => dispatch("close")}
    class="fixed left-0 top-0 w-full h-full z-10 flex items-center justify-center bg-black bg-opacity-40"
>
    <div
        in:scale
        class="rounded-md p-4 w-full max-w-sm bg-white z-40 drop-shadow-md"
    >
        <slot />
    </div>
</div>
