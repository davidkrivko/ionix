<script>
// @ts-nocheck


import {
  profile,
  first_name,
  logo,
  email,
  boiler_id,
  mobile_menu,
} from './stores/store';

import { onMount } from "svelte"; 
import axios from "axios";
import Dashboard from "./components/Dashboard.svelte";
import Header from './components/shared/Header.svelte';
import MobileMenu from './components/shared/MobileMenu.svelte';

onMount(()=>{

  loadProfile();
  
})

async function loadProfile() {
    try {
    const endpoint = '/api/users/me/'
    const response = await axios({
        url: endpoint,
        method: "get",

    });
    if(response.status === 200) {
            $profile = response.data.data.profile;
            $first_name = response.data.data.first_name;
            $logo = response.data.data.logo;
            $email = response.data.data.email;
            $boiler_id = response.data.data.boiler_id;
        }
    } catch(error) {
            console.log(error)
    }
};
</script>

<!-- <Header /> -->
{#if $mobile_menu}
    <MobileMenu />
{/if}
<div class="bg-transparent px-4 py-4">
  <Dashboard />
</div>