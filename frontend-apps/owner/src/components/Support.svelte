<script>
import { onMount } from "svelte";
import { fade, slide } from "svelte/transition";
import axios from 'axios';
import { message, messenger } from '../stores/store';
import { getCsrfCookieValue } from '../lib/utils';


// form data
let subject, email;
let request_body;
let freeze = false;

onMount(async() => {
    loadRequestHistory();
});

let requests = [];
let support_form = false;
let success_form = false;

async function loadRequestHistory() {
  try {
  const endpoint = `/api/support/`;
  const response = await axios({
      url: endpoint,
      method: "get",

  });
  if(response.status === 200) {
        const res = response.data;
        requests = res;
      }
  } catch(error) {
        console.log(error)
  }
};


async function submitSupportRequest() {

    const validate = validateForm();
    $message = "Please fill in all required fields";
    $messenger = true;
    if (!validate) return;

    try {
        const endpoint = '/api/support/';
        const csrfcookie = getCsrfCookieValue();
        const data = {
            "subject": subject,
            "request": request_body,
            "email": email,
            };
        const response = await axios({
            url: endpoint,
            method: "post",
            data: data,
            headers: {
            'X-CSRFToken': csrfcookie
            }

        });
        if(response.status === 201) {
            resetForm();
            success_form = true;
            setTimeout(() => {success_form = false; loadRequestHistory();}, 5000)
            }
    } catch(error) {
            console.log(error)
    }
}

function validateForm() {
    freeze = false;
    if (subject === undefined || subject === null || subject?.length < 5) {
        subject = null;
        freeze = true;
    }
    if (email === undefined || email === null || email?.length < 5) {
        email = null;
        freeze = true;
    }
    return !freeze;
}
function resetForm() {
    subject = '';
    request_body = '';
    support_form = false;
}

let item_details = Array(requests).fill(null).map((x, index) => false)
</script>



<div class="w-full px-8 max-w-lg " in:fade>
    <div class="text-lg font-semibold pb-6">
        TECHNICAL ASSISTANCE
    </div>
    <div class="py-4">
        <button on:click={() => support_form = true}
        class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">New case</button>
    </div>
    {#if success_form}
        <div class="rounded-md mt-4 px-6 py-6 bg-white shadow-md text-center" in:slide>
            Thank you! We've received your request and will reach you via email within one working day.
        </div>
    {/if}
    {#if support_form}
        <div class="grid grid-cols-1 rounded-md mt-4 px-6 py-6 bg-white shadow-md" in:slide>
            <div class="flex flex-col gap-y-4">
                <div class="font-semibold text-gray-700">
                    Subject *:
                </div>
                <div class="">
                    <input type="text" class:error={subject === null} bind:value={subject} placeholder="e.x. Heating problem" class="px-2 border-1 w-full h-10 ring-1 ring-gray-600">
                </div>
                <div class="font-semibold text-gray-700">
                    Email *:
                </div>
                <div class="">
                    <input type="email" class:error={email === null} bind:value={email} placeholder="email@example.com" class="px-2 border-1 w-full h-10 ring-1 ring-gray-600">
                </div>
            </div>
            <div class="flex flex-col gap-y-4 mt-6">
                <div class="font-semibold text-gray-700">
                    Detailed description:
                </div>
                <div>
                    <textarea class:error={request_body === null} bind:value={request_body} placeholder="Please, add more details here" class="p-2 border-1 h-16 w-full ring-1 ring-gray-600"></textarea>
                </div>
            </div>
            <div class="py-4 flex flex-row gap-x-4">
                <button on:click={() => submitSupportRequest()}
                class="ring-2 text-sm ring-blue-400 rounded-md px-4 py-1 active:ring-blue-700">
                    Submit
                </button>
                <button on:click={() => resetForm()}
                    class="ring-2 text-sm ring-green-400 rounded-md px-4 py-1 active:ring-green-700">
                        Cancel
                </button>
            </div>
        </div>
    {/if}
    
    <div class="mt-14 text-lg py-4 underline">My requests:</div>
    {#each requests as request, index }
    <div on:click={() => item_details[index] = !item_details[index]}
    in:slide class="grid grid-cols-3 px-4 py-3 mt-4 gap-x-4 shadow-md support rounded-md bg-white text-black cursor-pointe">
        <div class="overflow-auto">
            {request.subject}
        </div>
        <div class="">
            {new Date(request.created_at).toLocaleDateString('en-US')}
        </div>
        <div>
            <span class:bg-purple-400={request.status === 'P'} class:bg-green-600={request.status === 'R'} class:bg-gray-600={request.status === 'C'}
            class="text-white px-2 py-1 rounded-md">{request.status === 'P' ? 'Pending' : request.status === 'R' ? 'Resolved' : 'Closed'}</span>
        </div>
    </div>
    {#if item_details[index]}
        <div transition:slide class="px-4 py-3 mt-2 rounded-sm shadow-sm bg-white text-black">
            {request.request}
        </div>
    {/if}
    {:else}
    <div class="mt-2">
        No records yet.
    </div>
    {/each}

</div>


<style>
    .support {
        grid-template-columns: 1fr auto auto;
    }
</style>