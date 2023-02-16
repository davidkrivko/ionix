<script>
// @ts-nocheck


import {
  profile,
  first_name,
  logo,
  is_guest,
  email,
  first_login,
  selected_component,
} from './stores/store';

import { onMount } from "svelte"; 
import axios from "axios";
import TenantDashboard from "./components/Tenant/TenantDashboard.svelte";

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
            console.log(response.data)
            $profile = response.data.data.profile;
            $first_name = response.data.data.first_name;
            $logo = response.data.data.logo;
            $email = response.data.data.email;
            $is_guest = response.data.data.is_guest;
            $first_login = response.data.data.password_reset_needed;
            if ($first_login === true && $is_guest === false) {
              $selected_component = 'profile';
            }
        }
    } catch(error) {
            console.log(error)
    }
};
</script>


<main class="flex flex-col h-screen items-stretch">
  <TenantDashboard />
</main>
  




<style>
  @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

  :global(body) {
    font-family: 'Cairo', sans-serif;
  }
  :root {
  --light: #edf2f9;
  --dark: #152e4d;
  --darker: #12263f;
  /*  */
  --color-primary: var(--color-cyan);
  --color-primary-50: var(--color-cyan-50);
  --color-primary-100: var(--color-cyan-100);
  --color-primary-light: var(--color-cyan-light);
  --color-primary-lighter: var(--color-cyan-lighter);
  --color-primary-dark: var(--color-cyan-dark);
  --color-primary-darker: var(--color-cyan-darker);
  /*  */
  --color-green: #16a34a;
  --color-green-50: #f0fdf4;
  --color-green-100: #dcfce7;
  --color-green-light: #22c55e;
  --color-green-lighter: #4ade80;
  --color-green-dark: #15803d;
  --color-green-darker: #166534;
  /*  */
  --color-blue: #2563eb;
  --color-blue-50: #eff6ff;
  --color-blue-100: #dbeafe;
  --color-blue-light: #3b82f6;
  --color-blue-lighter: #60a5fa;
  --color-blue-dark: #1d4ed8;
  --color-blue-darker: #1e40af;
  /*  */
  --color-cyan: #0891b2;
  --color-cyan-50: #ecfeff;
  --color-cyan-100: #cffafe;
  --color-cyan-light: #06b6d4;
  --color-cyan-lighter: #22d3ee;
  --color-cyan-dark: #0e7490;
  --color-cyan-darker: #155e75;
  /*  */
  --color-teal: #0d9488;
  --color-teal-50: #f0fdfa;
  --color-teal-100: #ccfbf1;
  --color-teal-light: #14b8a6;
  --color-teal-lighter: #2dd4bf;
  --color-teal-dark: #0f766e;
  --color-teal-darker: #115e59;
  /*  */
  --color-fuchsia: #c026d3;
  --color-fuchsia-50: #fdf4ff;
  --color-fuchsia-100: #fae8ff;
  --color-fuchsia-light: #d946ef;
  --color-fuchsia-lighter: #e879f9;
  --color-fuchsia-dark: #a21caf;
  --color-fuchsia-darker: #86198f;
  /*  */
  --color-violet: #7c3aed;
  --color-violet-50: #f5f3ff;
  --color-violet-100: #ede9fe;
  --color-violet-light: #8b5cf6;
  --color-violet-lighter: #a78bfa;
  --color-violet-dark: #6d28d9;
  --color-violet-darker: #5b21b6;
}
</style>
