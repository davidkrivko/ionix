<script>
  import {
    first_name,
    logo,
    selected_dashboard_component,
    mobile_menu,
} from '../../stores/store';

</script>

  <header class="w-full flex-shrink-0">
    <div class="flex flex-row items-center py-4 border-b max-w-screen-xl px-8">
        <div on:click={() => $selected_dashboard_component = 'rooms'}
        class="hidden md:block text-gray-300 text-xl cursor-pointer">
        Ioniqbox Staff
        </div>
        <div class="md:hidden ml-2 cursor-pointer" on:click={() => $mobile_menu = true}>
          <svg class="w-12 fill-current text-gray-50" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><g><path d="M69,50c0-1.657-1.343-3-3-3H26c-1.657,0-3,1.343-3,3s1.343,3,3,3h40C67.657,53,69,51.657,69,50z"></path><path d="M26,65c-1.657,0-3,1.343-3,3s1.343,3,3,3h32c1.657,0,3-1.343,3-3s-1.343-3-3-3H26z"></path><path d="M77,32c0-1.657-1.343-3-3-3H26c-1.657,0-3,1.343-3,3s1.343,3,3,3h48C75.657,35,77,33.657,77,32z"></path></g></svg>
        </div>
         <!-- User avatar button -->
        <div class="flex flex-grow justify-end md:hidden">
          <div class="flex mr-4 text-gray-50 items-center">{$first_name}</div>
          <button on:click={() => $selected_dashboard_component = 'profile'}
            type="button"
            class="transition-opacity duration-200 rounded-full dark:opacity-75 dark:hover:opacity-100 focus:outline-none focus:ring dark:focus:opacity-100"
          >
            <span class="sr-only">User menu</span>
            <img class="w-10 h-10 rounded-full" src="{$logo || '/static/dashboard/img/user.svg'}" alt="User" />
          </button>
        </div>
        <div class="flex flex-row flex-grow justify-end">
          <form action="/logout/" method="GET">
            <button class="btn-secondary px-4 py-1.5 text-sm">Logout</button>
          </form>
        </div>
    </div>
  </header>


<style>
  header {
    background-color: rgb(49, 58, 70);
  }
</style>