<script>
import axios from 'axios';
// import { onMount } from 'svelte';
import { fade } from 'svelte/transition';

import { getCsrfCookieValue } from '../lib/utils';
import { first_name, email } from '../stores/store';

let new_password, new_password1, old_password;
let freeze = false;
const current_email = $email;

async function updatePassword() {

    const validation =  validatePasswordUpdateForm();

    if (validation === false) return;
    try {
        const endpoint = '/api/users/password/update/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
        "old_password": old_password,
        "new_password": new_password,
        }
        const response = await axios({
            url: endpoint,
            method: "post",
            data: data,
            headers: {
            'X-CSRFToken': csrfcookie
            }

        });
        if(response.status === 200) {
            
            location.reload();
            }
    } catch(error) {
            console.log(error)
            if (error.response.status === 403) {
                old_password = null;
            }
    }
};


async function updateName() {

    const validation =  validateNameForm();


    if (validation === false) return;
    let new_email;
    if ($email !== current_email) {
        new_email = $email;
    }
    try {
        const endpoint = '/api/users/owner/profile/update/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
        "first_name": $first_name,
        "email": new_email,
        }
        const response = await axios({
            url: endpoint,
            method: "post",
            data: data, 
            headers: {
            'X-CSRFToken': csrfcookie
            }

        });
        if(response.status === 200) {
            location.reload()
            }
    } catch(error) {
            console.log(error)
    }
};

function validatePasswordUpdateForm() {
    freeze = false;
    if (old_password?.length === 0 || old_password === undefined  || old_password === null) {
        freeze = true;
        old_password = null;
    } 
    if (new_password?.length === 0 || new_password === undefined || new_password === null) {
        freeze = true;
        new_password = null;
    }
    if (new_password !== new_password1) {
        freeze = true;
        new_password = null;
        new_password1 = null;
    }

    return !freeze;
}

function validateNameForm() {
    if ($first_name.length === 0) { 
        $first_name = null;
        return false;
    }
    return true;
}
</script>



<div class="flex flex-col h-full" in:fade>
    <div class="w-full gradient py-6 px-4 md:px-8 rounded-tr-2xl relative">
        <div class="py-4 flex flex-row gap-x-4 items-center">
            <span class="text-3xl font-bold text-white tracking-wider">
                Hello, {$first_name}
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
            Personal settings
        </div>
    </div>
    <div class="px-4 md:px-12 py-12 bg-gray-50 rounded-br-2xl flex flex-col flex-grow">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 max-w-md gap-y-3">
            <div class="mr-2">Name:</div>
            <div>
                <input class="ring-1 ring-gray-700 px-4 py-1.5 text-sm inline-flex w-full" 
                class:error={$first_name === null} bind:value={$first_name}>
            </div>
            <div class="mr-2">Email:</div>
                <div>
                    <input class="ring-1 ring-gray-700 px-4 py-1.5 text-sm inline-flex w-full" 
                bind:value={$email}>
            </div>
        </div>
        <div class="mt-3">
            <button on:click={() => updateName()}
            class="text-sm px-4 py-2 shadow-md active:shadow-sm bg-gray-100 text-gray-700 active:ring-blue-700">Save</button>
        </div>
        <div class="pt-10 font-medium pb-2">Update password</div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 max-w-md gap-y-3 mt-4">
            <div class="" >Current password:</div>
            <div><input type="password" class="ring-1 ring-gray-700 px-4 py-1.5 text-sm inline-flex w-full"
                class:error={old_password === null} bind:value={old_password}></div>
            <div class="">New password:</div>
            <div><input type="password" class="ring-1 ring-gray-700 px-4 py-1.5 text-sm inline-flex w-full" 
                class:error={new_password === null} bind:value={new_password}></div>
                <div class="">New password again:</div>
                <div><input type="password" class="ring-1 ring-gray-700 px-4 py-1.5 text-sm inline-flex w-full" 
                    class:error={new_password1 === null} bind:value={new_password1}></div>
        </div>
        <div class="mt-3">
            <button on:click={() => updatePassword()}
            class="text-sm px-4 py-2 shadow-md active:shadow-sm bg-gray-100 text-gray-700 active:ring-blue-700">Update</button>
        </div> 
    </div>
</div>


<style>
    .gradient {
        background-image: radial-gradient( circle 732px at -23.9% -25.1%,  rgba(30,39,107,1) 6.1%, rgba(188,104,142,1) 100.2% );
    }

</style>