<script>
import axios from 'axios';
import { onMount } from 'svelte'; 
import { slide, fade } from 'svelte/transition';
import { getCsrfCookieValue } from '../../lib/utils';
import { createEventDispatcher } from 'svelte';
import ConfirmPopup from '../shared/ConfirmPopup.svelte';
import ResetEmailPopup from './ResetEmailPopup.svelte';

import Select from 'svelte-select';
import { 
    message,
    messenger,
    } from '../../stores/store';

export let apartment;


const dispatch = createEventDispatcher();

let freeze = true;
let email_reset_popup = false;

let new_tenant_name;
let new_tenant_email;
let tenant_creation_form = false;
let rooms = [];
let selected_rooms = [];

onMount(() => {
    fetchTenants();
    loadRooms();
})

let tenants = [];

async function fetchTenants() {
    try {
        const endpoint = `/api/users/owner/tenants/?apartment_id=${apartment.id}`;
        const response = await axios({
            url: endpoint,
            method: "get",
        });
        if(response.status === 200) {
                tenants = response.data;
            }
    } catch(error) {
            console.log(error)
    }
};

async function loadRooms() {
  try {
  const endpoint = `/api/users/owner/apartment/${apartment.id}/`;
  const response = await axios({
      url: endpoint,
      method: "get",

  })
  if (response.status === 200) {
      const res = response.data;
        rooms = res.map(x => { return {value: x.id, label: x.room_type} })
    //   return rooms;
  }
  } catch(error) {
        console.log(error)
  }
};

// async function loadRoomsChoices() {
//     let res = await loadRooms();
//     return res;
//   }

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
            tenant_creation_form = false;
            fetchTenants();
            dispatch('change');
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


async function deleteTenant(tenant_id, index) {

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
        remove_popup_items[index] = false;
        fetchTenants();
        }
} catch(error) {
        console.log(error)
}
};


async function resendLink(tenant, email, index) {

try {
    const endpoint = '/api/users/owner/tenant/reset/';
    const csrfcookie = getCsrfCookieValue();
    const data = {
        "id": tenant.id,
        "email": email,
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
            reset_popup_items[index] = false;
            $message = "Password reset link was sent to the user"
            $messenger = true;
        }
    } catch(error) {
            console.log(error)
    }
};


async function makeLeaseHolder(tenant_id) {

    try {
        const endpoint = '/api/users/owner/tenant/leaseholder/';
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
                $message = "Tenant was successfully set as a leaseholder"
                $messenger = true;
                dispatch('change')
            }
    } catch(error) {
            console.log(error)
    }
};


function copyLink(value) {
    navigator.clipboard.writeText(value)
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

function handleRoomsSelection(e) {
    console.log(e.detail)
    const selection = e.detail;
    selected_rooms = []
    if (selection === null) return
    selection.map(x => { selected_rooms.push(x.value) })
    console.log("selected_rooms", selected_rooms)
}

let remove_popup_items = Array(tenants).fill(null).map((x, index) => false);
let reset_popup_items = Array(tenants).fill(null).map((x, index) => false);
</script>

<div>
    <!-- Tenant list  -->
    <div class="mt-4 bg-white px-5 py-4 shadow-md rounded-md">
        <div class="py-2- mb-8 flex flex-row gap-x-4 items-center">
            <div>
            <button on:click={() => tenant_creation_form = !tenant_creation_form}
                class="bg-gradient-to-b from-gray-300 to-gray-50 shadow-sm px-4 py-2 text-sm flex flex-row items-center gap-x-3 ring-info-light">
                    <span class="text-gray-800">
                        {#if tenant_creation_form === false}
                        Add new tenant
                    {:else}
                        Close
                    {/if}
                    </span>
            </button>
            </div>
        </div>
            {#if tenant_creation_form === true}
            <div transition:slide class="grid grid-cols-1 md:grid-cols-2 my-8 py-2 pr-2 gap-y-4 max-w-sm">
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
                <div>
                    <input bind:value={new_tenant_email} class:error={new_tenant_email===null} 
                    placeholder="newtenant@gmail.com"
                    type="email" name="email" class="px-2 w-full h-8 ring-1 ring-gray-600">
                </div>
                <div class="">
                    <label for="rooms" class="">Selected rooms: *</label>
                </div>
                <div class="themed-selection">
                    <Select items={rooms} isMulti={true} on:select={handleRoomsSelection} />
                </div>
                <div>
                    <button on:click={()=> createUser()}
                        class="btn-primary px-4 py-2">
                        Create
                    </button>
                </div>
            </div>
            {/if}
            <div class="bg-white grid grid-cols-2 md:grid-cols-4 gap-x-3 mb-3">
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
            </div>
            <div class="bg-white grid grid-cols-2 md:grid-cols-4 gap-x-3 gap-y-2">
            {#each tenants as tenant, index (tenant.id) }
                <div>
                    {tenant.first_name}
                </div>
                <div>
                    {new Date(tenant.created_at).toLocaleDateString('en-US')}
                </div>
                <div class="flex flex-row overflow-hidden">
                    {tenant.email}
                </div>
                <div class="flex flex-row gap-x-1">
                    <div class="w-6 cursor-pointer" on:click={() => makeLeaseHolder(tenant.id)} title="Set as leaseholder">
                        <svg class="fill-current text-gray-600" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><switch><foreignObject requiredExtensions="http://ns.adobe.com/AdobeIllustrator/10.0/" x="0" y="0" width="1" height="1"></foreignObject><g i:extraneous="self"><g><rect x="29.8" y="45.7" width="31.8" height="4.6"></rect><rect x="29.8" y="35.2" width="31.8" height="4.6"></rect><rect x="29.8" y="24.6" width="31.8" height="4.6"></rect><rect x="40.7" y="66.8" width="20.9" height="4.6"></rect><rect x="29.8" y="56.3" width="31.8" height="4.6"></rect><path d="M92.7,7.2L45.9,2.5c-2.4-0.3-4.6,1.5-4.9,4l-0.6,6.6H22.2c-2.5,0-4.5,2-4.5,4.5v45.7c-8.2,1.4-14.4,8.4-14.4,17     c0,9.5,7.7,17.2,17.2,17.2c8.6,0,15.7-6.3,17-14.6h31.7c2.5,0,4.5-2,4.5-4.5v-3l12.1,1.2c2.5,0.2,4.7-1.6,4.9-4l6-60.6     C96.9,9.6,95.1,7.4,92.7,7.2z M22,89.8v1.7c0,0.4-0.3,0.7-0.7,0.7h-1.9c-0.4,0-0.7-0.3-0.7-0.7v-1.9c-1.6-0.5-3-1.4-3.7-2     c-0.4-0.3-0.4-0.9-0.1-1.3l1.3-1.3c0.3-0.3,0.8-0.3,1.2-0.1c0.8,0.6,2.1,1.4,3.3,1.4c2.3,0,2.3-1.4,2.3-1.9     c0-0.8-0.2-1.5-2.8-2.4c-3.6-1.3-5.5-3.3-5.5-6.1c0-2.5,1.6-4.4,4-5.1V69c0-0.4,0.3-0.7,0.7-0.7h1.9c0.4,0,0.7,0.3,0.7,0.7v1.7     c1.4,0.3,2.5,0.9,3.2,1.4c0.4,0.3,0.5,0.9,0.1,1.3L24,74.8c-0.3,0.3-0.8,0.4-1.1,0.1c-0.6-0.4-1.4-0.8-2.3-0.8     c-0.6,0-2.4,0.2-2.4,1.8c0,0.5,0,1.6,3.1,2.7c1.5,0.6,5.2,1.8,5.2,5.8C26.5,87.3,24.8,89.3,22,89.8z M69.1,78.3H37.6     c-0.9-8-7.3-14.4-15.3-15.2V17.7h46.8V78.3z M86.1,72l-12.4-1.2v-6.9l5.7,0.5l0.5-4.6l-6.1-0.6v-6l6.7,0.7l0.5-4.6l-7.2-0.7v-6     l7.8,0.8l0.5-4.6L73.7,38v-6l8.8,0.9l0.5-4.6l-9.2-0.9v-6l9.8,1l0.4-4.6l-10.3-1c-0.4-2.1-2.2-3.7-4.4-3.7H44.9l0.6-6l46.5,4.6     L86.1,72z"></path></g></g></switch></svg>
                    </div>
                    <div on:click={() => reset_popup_items[index] = true} class="w-6 cursor-pointer" title="Resend the link">
                        {#if reset_popup_items[index]}
                        <ResetEmailPopup tenant={tenant} on:confirm={(e)=> resendLink(tenant, e.detail, index)}
                            on:cancel={() => reset_popup_items[index]= false}/>
                        {/if}
                        <span class="fill-current text-gray-600">
                            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" x="0px" y="0px" viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve"><path d="M73,12c-11.5,0-20.9,8.8-21.9,20H13c-4.4,0-8,3.6-8,8v40c0,4.4,3.6,8,8,8h66c4.4,0,8-3.6,8-8V51c4.9-4,8-10.1,8-17  C95,21.9,85.1,12,73,12z M13,36h38.1c0.6,6.9,4.4,12.8,9.9,16.4L47.3,64.2c-0.8,0.7-1.9,0.7-2.6,0L12.2,36.1C12.4,36,12.7,36,13,36z   M9,80V40c0-0.4,0.1-0.8,0.2-1.2L33.7,60L9.2,81.2C9.1,80.8,9,80.4,9,80z M79,84H13c-0.3,0-0.6,0-0.8-0.1l24.6-21.3l5.3,4.6  c1.1,1,2.5,1.5,3.9,1.5s2.8-0.5,3.9-1.5l5.3-4.6l24.6,21.3C79.6,84,79.3,84,79,84z M83,80c0,0.4-0.1,0.8-0.2,1.2L58.3,60l6.5-5.6  c2.5,1,5.3,1.6,8.2,1.6c3.6,0,7-0.9,10-2.4V80z M73,52c-9.9,0-18-8.1-18-18s8.1-18,18-18s18,8.1,18,18S82.9,52,73,52z M82.9,26.2  c0.8,0.8,0.8,2,0,2.8L70.2,41.8c-0.4,0.4-0.9,0.6-1.4,0.6s-1-0.2-1.4-0.6l-4.2-4.2c-0.8-0.8-0.8-2,0-2.8c0.8-0.8,2.1-0.8,2.8,0  l2.8,2.8l11.3-11.3C80.8,25.4,82.1,25.4,82.9,26.2z"></path></svg>
                        </span>
                    </div>
                    <div on:click={() => copyLink(tenant?.access_link)}
                        class="w-6 cursor-pointer" title="Copy link to a clipboard">
                            <svg class="fill-current text-gray-600 active:text-green-400 transform transition-colors" viewBox="0 0 100 100" x="0px" y="0px"><path d="M80.36,12H38.42a7.64,7.64,0,0,0-7.64,7.64V30.78H19.64A7.64,7.64,0,0,0,12,38.41v42A7.64,7.64,0,0,0,19.64,88h42a7.64,7.64,0,0,0,7.63-7.64V69.22H80.36A7.64,7.64,0,0,0,88,61.58V19.64A7.64,7.64,0,0,0,80.36,12ZM65.22,67.16s0,0,0,.06,0,0,0,.06V80.36A3.64,3.64,0,0,1,61.59,84h-42A3.64,3.64,0,0,1,16,80.36v-42a3.64,3.64,0,0,1,3.64-3.63h42a3.64,3.64,0,0,1,3.63,3.63ZM84,61.58a3.64,3.64,0,0,1-3.64,3.64H69.22V38.41a7.64,7.64,0,0,0-7.63-7.63H34.78V19.64A3.64,3.64,0,0,1,38.42,16H80.36A3.64,3.64,0,0,1,84,19.64Z"></path></svg>
                    </div>
                    <div on:click={() => remove_popup_items[index] = true} title="Delete tenant" class="w-5 cursor-pointer">
                        {#if remove_popup_items[index]}
                        <ConfirmPopup 
                        note={'This action will remove tenant account from the system and they will no longer have access to room thermostats.'}
                        on:confirm={()=>  deleteTenant(tenant.id, index)} 
                        on:cancel={()=> remove_popup_items[index] = false } />
                        {/if}
                        <svg class="fill-current text-gray-600 active:text-red-400 transform transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" x="0px" y="0px"><defs><style>.cls-1{fill:none;}</style></defs><g data-name="Layer 2"><g data-name="Layer 1"><path d="M76.65,100H23.35a8.93,8.93,0,0,1-8.91-8.92V30.42a8.93,8.93,0,0,1,8.91-8.92h53.3a8.93,8.93,0,0,1,8.91,8.92V91.08A8.93,8.93,0,0,1,76.65,100ZM23.35,27.91a2.52,2.52,0,0,0-2.51,2.51V91.08a2.51,2.51,0,0,0,2.51,2.51h53.3a2.51,2.51,0,0,0,2.51-2.51V30.42a2.52,2.52,0,0,0-2.51-2.51Z"></path><path d="M92.45,27.91H7.55v-3.2A19.25,19.25,0,0,1,26.77,5.48H73.23A19.25,19.25,0,0,1,92.45,24.71ZM14.36,21.5H85.64a12.84,12.84,0,0,0-12.41-9.61H26.77A12.84,12.84,0,0,0,14.36,21.5Z"></path><path d="M34,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,34,82Z"></path><path d="M50,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,50,82Z"></path><path d="M66,82a3.2,3.2,0,0,1-3.2-3.2V42.65a3.2,3.2,0,0,1,6.4,0v36.1A3.2,3.2,0,0,1,66,82Z"></path><path d="M68.05,6.41H32A3.21,3.21,0,0,1,32,0h36.1a3.21,3.21,0,0,1,0,6.41Z"></path><rect class="cls-1" width="100" height="100"></rect></g></g></svg>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</div>


<style>
.themed-selection {
    --height: 32px;
    --borderFocusColor: black;
    --inputPadding: 0.2rem;
    --borderRadius: 0;
}
</style>