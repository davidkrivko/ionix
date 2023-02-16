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

<div in:fade class="mx-auto w-full max-w-screen-sm">

    <div class="mb-12 font-semibold text-lg">MY PROFILE</div>

    <div class="">
        <div class="grid grid-cols-2 grid-flow-row gap-x-0 gap-y-4">
            <div class="mr-2">Name:</div>
            <div><input class="border-2 w-10/12 rounded-md px-3" 
                class:error={$first_name === null} bind:value={$first_name}></div>
            <div class="mr-2">Email:</div>
                <div><input class="border-2 w-10/12 rounded-md px-3" 
                bind:value={$email}></div>
        </div>
        <div class="mt-3">
            <button on:click={() => updateName()}
            class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">Save</button>
        </div>
        <div class="mt-10 font-semibold mb-2">Update password</div>
        <div class="grid grid-cols-2 grid-flow-row gap-y-4 gap-x-0 mt-4">
            <div class="" >Current password:</div>
            <div><input type="password" class="border-2 w-10/12 rounded-md px-3"
                class:error={old_password === null} bind:value={old_password}></div>
            <div class="">New password:</div>
            <div><input type="password" class="border-2 w-10/12 rounded-md px-3" 
                class:error={new_password === null} bind:value={new_password}></div>
                <div class="">New password again:</div>
                <div><input type="password" class="border-2 w-10/12 rounded-md px-3" 
                    class:error={new_password1 === null} bind:value={new_password1}></div>
        </div>
        <div class="mt-3">
            <button on:click={() => updatePassword()}
            class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">Update</button>
        </div> 
        <div class="items-center">
            <div class="py-6">
                <form action="/logout/" method="GET">
                    <button type="submit" class="px-4 py-1 rounded-md ring-red-400 ring-2 text-sm">Logout</button>
                </form>
            </div>
        </div>

    </div>

</div>

<style>

</style>