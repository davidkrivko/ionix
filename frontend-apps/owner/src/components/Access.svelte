<script>
import axios from 'axios';
import { onMount } from 'svelte'; 
import { slide, fade } from 'svelte/transition';
import { getCsrfCookieValue } from '../lib/utils';
import { 
    qcodepopup,
    message,
    messenger,
 } from '../stores/store';

import QrCode from './subcomponents/QrCode.svelte';
let current_access_link;

let freeze = true;

let new_tenant_name;
let new_tenant_email;
let guest_creation_form = false;
let tenant_creation_form = false;
let rooms = [];
let selected_rooms = [];

onMount(() => {
    fetchTenants(true);
    fetchTenants();
    fetchRooms();
})


let guest_tenants = [];
let tenants = [];

async function fetchTenants(guests=false) {
    try {
        const endpoint = `/api/users/owner/tenants/?guests=${guests}`;
        // const csrfcookie = getCsrfCookieValue();
        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
            console.log(response.data)
            if (guests === true) {
                guest_tenants = response.data;
            } else {
                tenants = response.data;
                }
            }
    } catch(error) {
            console.log(error)
    }
};

async function fetchRooms() {
    try {
        const endpoint = `/api/users/owner/rooms/all/`;
        // const csrfcookie = getCsrfCookieValue();
        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
            rooms = response.data;
            }
    } catch(error) {
            console.log(error);
    }
};

function createGuest() {
    createUser(true);
}

async function createUser(is_guest = false) {

    const validation =  validateTenantCreateForm(is_guest);

    if (validation === false) return;
    
    try {
        const endpoint = '/api/users/owner/tenants/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
            "first_name": new_tenant_name,
            "is_guest": is_guest,
            "rooms_ids": selected_rooms,
            "email": new_tenant_email,
        }
        console.log("data", data)
        const response = await axios({
            url: endpoint,
            method: "post",
            data: data,
            headers: {
            'X-CSRFToken': csrfcookie
            }

        });
        if(response.status === 201) {
            if (is_guest) {
                guest_creation_form = false;
                fetchTenants(true);
            } else {
                tenant_creation_form = false;
                fetchTenants(false);
                }
            new_tenant_email = '';
            new_tenant_name = '';
            selected_rooms = [];
            }
    } catch(error) {
            console.log(error)
            $message = "Email already exists or incorrect";
            $messenger = true;
            new_tenant_email = null;
            return false;
    };
};


async function deleteTenant(tenant_id) {

try {
    const endpoint = '/api/users/owner/tenant/delete/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
        "id": tenant_id,
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
        fetchTenants(true);
        fetchTenants();
        }
} catch(error) {
        console.log(error)
}
};


async function resendLink(tenant_id) {

try {
    const endpoint = '/api/users/owner/tenant/reset/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
        "id": tenant_id,
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
            $message = "Password reset link was sent to the user"
            $messenger = true;
        }
} catch(error) {
        console.log(error)
}
};


function copyLink(value) {
    navigator.clipboard.writeText(value)
}

function showQrCode(link) {
    current_access_link = link;
    $qcodepopup = true;
}


function validateTenantCreateForm(is_guest=false) {
    freeze = false;
    if (new_tenant_name?.length === 0 || new_tenant_name === undefined  || new_tenant_name === null) {
        freeze = true;
        new_tenant_name = null;
    } 
    if (is_guest === false) {
        if (new_tenant_email?.length === 0 || new_tenant_email === undefined  || new_tenant_email === null) {
            freeze = true;
            new_tenant_email = null;
        } 
    }   
    return !freeze;
}

</script>

<div in:fade class="max-w-screen-xl">
    {#if $qcodepopup === true}
        <QrCode link={current_access_link} />
    {/if}

    <div class="text-md font-semibold">
        SHARED ACCESS
    </div>
    <!-- Guest list  -->
    <div class="mt-4 bg-white px-5 py-4 shadow-md rounded-md">
        <div class="py-2- mb-8 flex flex-row gap-x-4 items-center">
            <div>
                <button on:click={() => guest_creation_form = !guest_creation_form}
                class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">
                {#if !guest_creation_form}
                    Add new guest
                {:else}
                    Close
                {/if}
                </button>
            </div>
        </div>
            {#if guest_creation_form === true}
            <div transition:slide class="grid grid-cols-1 md:grid-cols-2 py-2 pr-2my-8 gap-y-6 max-w-md">
                <div>
                    <label for="name" class="">Guest name:</label>
                </div>
                <div class="">
                    <input bind:value={new_tenant_name} class:error={new_tenant_name===null} 
                    type="text" name="name" class="px-2 w-full h-8 ring-1 ring-gray-600">
                </div>
                <div class="">
                    <label for="rooms" class="">Selected rooms:</label>
                </div>
                <div>
                    <select multiple bind:value={selected_rooms} name="rooms"
                    class="px-2 w-full h-24 overflow-y-auto py-2 ring-1 ring-gray-600">
                        {#each rooms as obj}
                            <option value="{obj.id}">{obj.name}</option>
                        {/each} 
                    </select>
                </div>
                <div>
                    <button on:click={()=> createGuest()}
                    class="ring-2 text-sm ring-green-400 rounded-md px-4 py-1 active:ring-green-700">Create</button>
                </div>
            </div>
            {/if}
            <div class="bg-white grid grid-cols-2 md:grid-cols-4 gap-3 rounded-md">
            <div class="font-semibold">
                Name
            </div>
            <div class="font-semibold">
                Date added
            </div>
            <div class="font-semibold">
                Access link
            </div>
            <div class="font-semibold">
                Action
            </div>
            {#each guest_tenants as guest }
                <div>
                    {guest.first_name}
                </div>
                <div>
                    {new Date(guest.created_at).toLocaleDateString('en-US')}
                </div>
                <div class="overflow-hidden flex flex-row gap-x-2">
                    <div on:click={() => copyLink(guest?.access_link)}
                    class="w-8 cursor-pointer" title="Copy link to a clipboard">
                        <svg class="fill-current text-gray-600 active:text-green-400 transform transition-colors" viewBox="0 0 100 100" x="0px" y="0px"><path d="M80.36,12H38.42a7.64,7.64,0,0,0-7.64,7.64V30.78H19.64A7.64,7.64,0,0,0,12,38.41v42A7.64,7.64,0,0,0,19.64,88h42a7.64,7.64,0,0,0,7.63-7.64V69.22H80.36A7.64,7.64,0,0,0,88,61.58V19.64A7.64,7.64,0,0,0,80.36,12ZM65.22,67.16s0,0,0,.06,0,0,0,.06V80.36A3.64,3.64,0,0,1,61.59,84h-42A3.64,3.64,0,0,1,16,80.36v-42a3.64,3.64,0,0,1,3.64-3.63h42a3.64,3.64,0,0,1,3.63,3.63ZM84,61.58a3.64,3.64,0,0,1-3.64,3.64H69.22V38.41a7.64,7.64,0,0,0-7.63-7.63H34.78V19.64A3.64,3.64,0,0,1,38.42,16H80.36A3.64,3.64,0,0,1,84,19.64Z"></path></svg>
                    </div>
                    <div on:click={() => showQrCode(guest?.access_link)}
                    class="w-8 cursor-pointer" title="Show QR code with the link">
                        <svg class="fill-current text-gray-600 active:text-green-700 transform transition-colors"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.0" x="0px" y="0px" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve"><path d="M10,10v23.333h23.333V10H10z M26.667,26.667h-10v-10h10V26.667z"></path><path d="M10,66.666V90h23.333V66.666H10z M26.667,83.334h-10v-10h10V83.334z"></path><path d="M66.667,10v23.333H90V10H66.667z M83.333,26.667h-10v-10h10V26.667z"></path><polygon points="40,10 40,16.667 53.333,16.667 53.333,33.333 60,33.333 60,10 "></polygon><polygon points="46.667,83.334 46.667,66.666 40,66.666 40,90 53.333,90 53.333,83.334 "></polygon><rect x="83.333" y="40" width="6.667" height="13.334"></rect><polygon points="76.667,40 53.333,40 53.333,53.334 60,53.334 60,46.667 76.667,46.667 "></polygon><rect x="23.333" y="53.334" width="23.334" height="6.666"></rect><polygon points="40,23.333 40,40 10,40 10,60 16.667,60 16.667,46.667 46.667,46.667 46.667,23.333 "></polygon><path d="M73.333,56.666c-9.205,0-16.666,7.461-16.666,16.668C56.667,82.539,64.128,90,73.333,90C82.539,90,90,82.539,90,73.334  C90,64.127,82.539,56.666,73.333,56.666z M72.155,80.699l-8.838-8.84l3.535-3.535l5.303,5.303l7.659-7.66l3.535,3.535L72.155,80.699  z"></path></svg>
                    </div>
                </div>
                <div class="flex flex-row">
                    <button on:click={() => deleteTenant(guest.id)}
                    class="ring-2 text-sm ring-red-300 rounded-md px-4 py-1 active:ring-red-700">Delete</button>
                </div>
            {/each}
        
        </div>
    </div>
    <!-- Tenant list  -->
    <div class="mt-4 bg-white px-5 py-4 shadow-md rounded-md">
        <div class="py-2- mb-8 flex flex-row gap-x-4 items-center">
            <div>
                <button on:click={() => tenant_creation_form = !tenant_creation_form}
                class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">
                {#if tenant_creation_form === false}
                    Add new tenant
                {:else}
                    Close
                {/if}
            </button>
            </div>
        </div>
            {#if tenant_creation_form === true}
            <div transition:slide class="grid grid-cols-1 md:grid-cols-2 my-8 py-2 pr-2 gap-y-6 max-w-sm">
                <div>
                    <label for="name" class="">Tenant name: *</label>
                </div>
                <div>
                    <input bind:value={new_tenant_name} class:error={new_tenant_name===null} type="text" name="name"
                     class="px-2 w-full h-8 ring-1 ring-gray-600">
                </div>
                <div>
                    <label for="name" class="">Tenant email: *</label>
                </div>
                <div class="overflow-hidden">
                    <input bind:value={new_tenant_email} class:error={new_tenant_email===null} 
                    placeholder="newtenant@gmail.com"
                    type="email" name="email" class="px-2 w-full h-8 ring-2 ring-gray-600">
                </div>
                <div class="">
                    <label for="rooms" class="">Selected rooms: *</label>
                </div>
                <div>
                    <select multiple bind:value={selected_rooms} name="rooms"
                    class="px-2 w-full h-24 overflow-y-auto py-2 ring-1 ring-gray-600">
                        {#each rooms as obj}
                            <option value="{obj.id}">{obj.name}</option>
                        {/each} 
                    </select>
                </div>
                <div>
                    <button on:click={()=> createUser()}
                    class="ring-2 text-sm ring-green-400 rounded-md px-4 py-1 active:ring-green-700">Create</button>
                </div>
            </div>
            {/if}
            <div class="bg-white grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="font-semibold">
                    Name
                </div>
                <div class="font-semibold">
                    Date added
                </div>
                <div class="font-semibold">
                    Email
                </div>
                <div class="font-semibold">
                    Action
                </div>
            {#each tenants as tenant }
                <div>
                    {tenant.first_name}
                </div>
                <div>
                    {new Date(tenant.created_at).toLocaleDateString('en-US')}
                </div>
                <div class="flex flex-row overflow-hidden">
                    {tenant.email}
                </div>
                <div class="flex flex-row">
                    <div on:click={() => resendLink(tenant.id)} class="w-6 cursor-pointer" title="Resend the link">
                        <span class="mr-2 fill-current text-gray-600">
                            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><path d="M73,12c-11.5,0-20.9,8.8-21.9,20H13c-4.4,0-8,3.6-8,8v40c0,4.4,3.6,8,8,8h66c4.4,0,8-3.6,8-8V51c4.9-4,8-10.1,8-17  C95,21.9,85.1,12,73,12z M13,36h38.1c0.6,6.9,4.4,12.8,9.9,16.4L47.3,64.2c-0.8,0.7-1.9,0.7-2.6,0L12.2,36.1C12.4,36,12.7,36,13,36z   M9,80V40c0-0.4,0.1-0.8,0.2-1.2L33.7,60L9.2,81.2C9.1,80.8,9,80.4,9,80z M79,84H13c-0.3,0-0.6,0-0.8-0.1l24.6-21.3l5.3,4.6  c1.1,1,2.5,1.5,3.9,1.5s2.8-0.5,3.9-1.5l5.3-4.6l24.6,21.3C79.6,84,79.3,84,79,84z M83,80c0,0.4-0.1,0.8-0.2,1.2L58.3,60l6.5-5.6  c2.5,1,5.3,1.6,8.2,1.6c3.6,0,7-0.9,10-2.4V80z M73,52c-9.9,0-18-8.1-18-18s8.1-18,18-18s18,8.1,18,18S82.9,52,73,52z M82.9,26.2  c0.8,0.8,0.8,2,0,2.8L70.2,41.8c-0.4,0.4-0.9,0.6-1.4,0.6s-1-0.2-1.4-0.6l-4.2-4.2c-0.8-0.8-0.8-2,0-2.8c0.8-0.8,2.1-0.8,2.8,0  l2.8,2.8l11.3-11.3C80.8,25.4,82.1,25.4,82.9,26.2z"></path></svg>
                        </span>
                    </div>
                    <div on:click={() => copyLink(tenant?.access_link)}
                        class="w-6 cursor-pointer" title="Copy link to a clipboard">
                            <svg class="fill-current text-gray-600 active:text-green-400 transform transition-colors" viewBox="0 0 100 100" x="0px" y="0px"><path d="M80.36,12H38.42a7.64,7.64,0,0,0-7.64,7.64V30.78H19.64A7.64,7.64,0,0,0,12,38.41v42A7.64,7.64,0,0,0,19.64,88h42a7.64,7.64,0,0,0,7.63-7.64V69.22H80.36A7.64,7.64,0,0,0,88,61.58V19.64A7.64,7.64,0,0,0,80.36,12ZM65.22,67.16s0,0,0,.06,0,0,0,.06V80.36A3.64,3.64,0,0,1,61.59,84h-42A3.64,3.64,0,0,1,16,80.36v-42a3.64,3.64,0,0,1,3.64-3.63h42a3.64,3.64,0,0,1,3.63,3.63ZM84,61.58a3.64,3.64,0,0,1-3.64,3.64H69.22V38.41a7.64,7.64,0,0,0-7.63-7.63H34.78V19.64A3.64,3.64,0,0,1,38.42,16H80.36A3.64,3.64,0,0,1,84,19.64Z"></path></svg>
                    </div>
                    <div on:click={() => deleteTenant(tenant.id)} title="Delete tenant" class="w-5 cursor-pointer">
                        <svg class="fill-current text-gray-600 active:text-red-400 transform transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" x="0px" y="0px"><defs><style>.cls-1{fill:none;}</style></defs><g data-name="Layer 2"><g data-name="Layer 1"><path d="M76.65,100H23.35a8.93,8.93,0,0,1-8.91-8.92V30.42a8.93,8.93,0,0,1,8.91-8.92h53.3a8.93,8.93,0,0,1,8.91,8.92V91.08A8.93,8.93,0,0,1,76.65,100ZM23.35,27.91a2.52,2.52,0,0,0-2.51,2.51V91.08a2.51,2.51,0,0,0,2.51,2.51h53.3a2.51,2.51,0,0,0,2.51-2.51V30.42a2.52,2.52,0,0,0-2.51-2.51Z"></path><path d="M92.45,27.91H7.55v-3.2A19.25,19.25,0,0,1,26.77,5.48H73.23A19.25,19.25,0,0,1,92.45,24.71ZM14.36,21.5H85.64a12.84,12.84,0,0,0-12.41-9.61H26.77A12.84,12.84,0,0,0,14.36,21.5Z"></path><path d="M34,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,34,82Z"></path><path d="M50,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,50,82Z"></path><path d="M66,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,66,82Z"></path><path d="M68.05,6.41H32A3.21,3.21,0,0,1,32,0h36.1a3.21,3.21,0,0,1,0,6.41Z"></path><rect class="cls-1" width="100" height="100"></rect></g></g></svg>
                    </div>
                </div>
            {/each}
        
        </div>
    </div>
</div>


<style>
select {
    -webkit-appearance: none;
    overflow: hidden;
    overflow-wrap: break-word;
    appearance: none;
    background: transparent;
    resize: none;
    min-height: 16px;
    outline: none;
    transition-duration: 1s;
    transition-property: all;
    transition-timing-function: ease;
    border-radius: 3px;
    font-size: 16px;
}
</style>