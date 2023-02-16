<script>
import {
    message,
    messenger
} from '../../stores/store';

import { fly, slide } from 'svelte/transition'
import { onMount } from 'svelte'

onMount(() => {
    let active = setTimeout(() => {
        $messenger = false;
        }, 3000);
    return () => {clearTimeout(active); $message = undefined; };
})
</script>

<div in:fly out:slide
class="flex fixed flex-row w-full bg-white justify-center left-0 bottom-0 ring-1 ring-gray-200 ring-opacity-50 bg-opacity-90 py-4 px-6 z-50 shadow-2xl">
    <div class="font-bold text-gray-700 text-sm">{$message || ''}</div>
</div>
