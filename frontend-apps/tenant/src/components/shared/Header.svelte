<script>
  import {
    first_name,
    logo,
    selected_component,
    is_guest,
} from '../../stores/store';

</script>

  <header class="w-full flex-shrink-0">
    <div class="flex flex-row items-center py-2 border-b dark:border-primary-darker mx-auto max-w-screen-lg px-8">
        <div on:click={() => $selected_component = 'rooms'} class="hidden text-center text-lg cursor-pointer">
          <span>MY HOME</span>
        </div>
         <!-- User avatar button -->
        <div class="flex flex-row flex-grow justify-end">
          <div class="flex mr-4 items-center">{$is_guest === true ? 'Guest' : $first_name}</div>
          {#if $is_guest === false}
          <button on:click={() => $selected_component = 'profile'}
            type="button"
            class="transition-opacity duration-200 rounded-full dark:opacity-75 dark:hover:opacity-100 focus:outline-none focus:ring dark:focus:opacity-100"
          >
            <span class="sr-only">User menu</span>
            <img class="w-10 h-10 rounded-full" src="{$logo || '/static/dashboard/img/user.svg'}" alt="User" />
          </button>
          {/if}
        </div>

         
    </div>
  </header>