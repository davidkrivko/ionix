<script>
import axios from 'axios';

import { getCsrfCookieValue } from '../../lib/utils';
import { first_name, selected_component, email, first_login, is_guest } from '../../stores/store';

let new_password, new_password1, old_password;
let freeze = false;


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

async function setFirstPassword() {

const validation =  validatePasswordUpdateForm(true);

if (validation === false) return;
try {
    const endpoint = '/api/users/password/update/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
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
}
};


async function updateName() {

    const validation =  validateNameForm();

    if (validation === false) return;
    try {
        const endpoint = '/api/users/name/update/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
        "first_name": $first_name,
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
                console.log(response)
            }
    } catch(error) {
            console.log(error)
    }
};

function validatePasswordUpdateForm(skip_old = false) {
    freeze = false;
    if (!skip_old) {
        if (old_password?.length === 0 || old_password === undefined  || old_password === null) {
            freeze = true;
            old_password = null;
        } 
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
    console.log(new_password, old_password, new_password1)
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


<div class="px-6">
    <div class="text-xl font-semibold pb-10">My profile</div>
    <div class="my-4">{$email}</div>
    <div class="">
        <div class="grid grid-cols-2 grid-flow-row gap-x-0">
            <div class="mr-2">Name:</div>
            <div><input class="border-2 w-10/12 rounded-md px-3" 
                class:error={$first_name === null} bind:value={$first_name}></div>
        </div>
        <div class="mt-3">
            <button on:click={() => updateName()}
            class="ring-2 text-sm ring-blue-100 rounded-md px-4 py-1 active:ring-blue-400">Save</button>
        </div>
    
        {#if $is_guest === false && $first_login === true}
            <!-- Update password form -->
            <div class="mt-10 font-semibold text-lg">Set your first password</div>
            <div class="grid grid-cols-2 grid-flow-row gap-y-4 gap-x-0 mt-4">
                <div class="">New password:</div>
                <div><input type="password" class="border-2 w-10/12 rounded-md px-3" 
                    class:error={new_password === null} bind:value={new_password}></div>
                    <div class="">New password again:</div>
                    <div><input type="password" class="border-2 w-10/12 rounded-md px-3" 
                        class:error={new_password1 === null} bind:value={new_password1}></div>
            </div>
            <div class="mt-3">
                <button on:click={() => setFirstPassword()}
                class="ring-2 text-sm ring-blue-100 rounded-md px-4 py-1 active:ring-blue-400">Set password</button>
            </div> 
             <!-- Update password form -->
        {:else}
        <!-- Update password form -->
        <div class="mt-10 font-semibold text-lg">Update password</div>
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
            class="ring-2 text-sm ring-blue-100 rounded-md px-4 py-1 active:ring-blue-400">Update</button>
        </div> 
         <!-- Update password form -->
         {/if}
    
        <div class="mt-10 grid grid-cols-1 gap-y-4">
            <div>
                <button on:click={() => $selected_component = 'rooms'}
                class="ring-2 text-sm ring-gray-300 rounded-md px-4 py-1 active:ring-blue-400">
                    Back
                </button>  
            </div>
            <div>
                <form action="/logout" method="GET">
                    <button type="submit"
                    class="ring-2 text-sm ring-red-300 rounded-md px-4 py-1 active:ring-blue-400">
                        Logout
                    </button>
                </form> 
            </div>
    
        </div> 
    </div>
</div>



<style>

    :global(.error) {
        border: 2px solid rgb(206, 23, 23);
    }

</style>