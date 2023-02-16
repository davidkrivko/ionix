<script>
      import { fade } from "svelte/transition";
</script>

<div class="flex flex-col h-full" in:fade>
      <div class="w-full gradient py-6 px-4 md:px-8 rounded-tr-2xl relative">
          <div class="py-4 flex flex-row gap-x-4 items-center">
              <span class="text-3xl font-bold text-white tracking-wider">
                  Statistics
              </span>
              <div class="text-sm" title="Logout">
                <form action="/logout/" type="submit" method="GET">
                  <button class="cursor-pointer text-gray-600" title="Log out">
                      <svg class="w-10 fill-current text-gray-200" viewBox="0 0 80 80" x="0px" y="0px"><path d="M71,23.31V56.69a8.44,8.44,0,0,1-8.43,8.43H50a3.93,3.93,0,1,1,0-7.85H62.57a.58.58,0,0,0,.58-.58V23.31a.58.58,0,0,0-.58-.58H50a3.93,3.93,0,1,1,0-7.85H62.57A8.44,8.44,0,0,1,71,23.31Z"></path><path d="M51.38,40.49a3.93,3.93,0,0,1-3.92,3.93H22.39l8,7.95a3.91,3.91,0,0,1,0,5.55,3.91,3.91,0,0,1-5.54,0L10.14,43.27a4,4,0,0,1,0-5.56L24.8,23.07a3.93,3.93,0,0,1,6.7,2.77,3.9,3.9,0,0,1-1.16,2.78l-7.95,8H47.46A3.93,3.93,0,0,1,51.38,40.49Z"></path></svg>
                  </button>
                </form>
              </div>
          </div>
          <div class="text-xl text-gray-50 font-semibold mt-6 py-4 pb-10">
              Here lives your data
          </div>
      </div>
      <div class="px-4 md:px-12 py-12 bg-gray-50 rounded-br-2xl flex flex-col flex-grow">
            Not enough data. Please come back later...
      </div>
  </div>
  
  
  <style>
      .gradient {
            background: #4e54c8;  /* fallback for old browsers */
            background: -webkit-linear-gradient(to right, #8f94fb, #4e54c8);  /* Chrome 10-25, Safari 5.1-6 */
            background: linear-gradient(to right, #8f94fb, #4e54c8); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
      }
  
  </style>