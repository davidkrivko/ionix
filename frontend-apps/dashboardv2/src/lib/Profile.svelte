<script>
    import axios from "axios";
    // import { onMount } from 'svelte';
    import { fade, slide } from "svelte/transition";
    import { onMount } from "svelte";
    import { getCsrfCookieValue } from "../lib/utils";
    import { first_name, email } from "../lib/store";
    import { toast } from "@zerodevx/svelte-toast";
    import BackIco from "./icons/back.svg?raw";
    import { selected_component } from "./store";

    let new_password, new_password1, old_password;
    let freeze = false;
    const current_email = $email;

    let updatePasswordForm = false;

    onMount(() => {
        getUserData();
    });

    async function getUserData() {
        const endpoint = "/api/users/me/";

        try {
            const resp = await axios({
                url: endpoint,
                method: "GET",
            });
            if (resp.status === 200) {
                // console.log("User data", resp.data);
                const data = resp.data.data;
                $first_name = data.first_name;
                $email = data.email;
            }
        } catch (err) {
            console.log(err);
        }
    }

    async function updatePassword() {
        const validation = validatePasswordUpdateForm();

        if (validation === false) return;
        try {
            const endpoint = "/api/users/password/update/";
            const csrfcookie = getCsrfCookieValue();
            const data = {
                old_password: old_password,
                new_password: new_password,
            };
            const response = await axios({
                url: endpoint,
                method: "post",
                data: data,
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (response.status === 200) {
                location.reload();
            }
        } catch (error) {
            console.log(error);
            if (error.response.status === 403) {
                old_password = null;
            }
        }
    }

    async function updateName() {
        const validation = validateNameForm();
        if (validation === false) return;
        let new_email;
        if ($email !== current_email) {
            new_email = $email;
        }
        try {
            const endpoint = "/api/users/owner/profile/update/";
            const csrfcookie = getCsrfCookieValue();
            const data = {
                first_name: $first_name,
                email: new_email,
            };
            const response = await axios({
                url: endpoint,
                method: "post",
                data: data,
                headers: {
                    "X-CSRFToken": csrfcookie,
                },
            });
            if (response.status === 200) {
                toast.push("Profile was updated");
            }
        } catch (error) {
            console.log(error);
        }
    }

    function validatePasswordUpdateForm() {
        freeze = false;
        if (
            old_password?.length === 0 ||
            old_password === undefined ||
            old_password === null
        ) {
            freeze = true;
            old_password = null;
            toast.push("Old password is required");
        }
        if (
            new_password?.length === 0 ||
            new_password === undefined ||
            new_password === null
        ) {
            freeze = true;
            toast.push("New password cannot be empty");
        }
        if (new_password !== new_password1) {
            freeze = true;
            toast.push("New password fields should be equal");
        }

        return !freeze;
    }

    function validateNameForm() {
        if ($first_name?.length === 0) {
            $first_name = null;
            return false;
        }
        return true;
    }
</script>

<div class="flex flex-col h-full" in:fade>
    <div class="p-5 bg-base-100 drop-shadow-md rounded-xl text-sm">
        <div class="flex flex-row gap-x-3 items-center py-4">
            <button on:click={() => ($selected_component = 0)} class="w-5"
                >{@html BackIco}</button
            >
            <span class="font-semibold">Profile settings</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 max-w-md gap-y-3">
            <div class="mr-2">Name:</div>
            <div>
                <input
                    class="input input-sm input-bordered"
                    class:error={$first_name === null}
                    bind:value={$first_name}
                />
            </div>
            <div class="mr-2">Email:</div>
            <div>
                <input
                    class="input input-sm input-bordered"
                    bind:value={$email}
                />
            </div>
        </div>
        <div class="mt-3">
            <button on:click={() => updateName()} class="btn btn-outline btn-xs"
                >Save</button
            >
        </div>
        <button
            class="btn btn-link my-4 btn-xs -ml-3"
            on:click={() => (updatePasswordForm = true)}>Update password</button
        >

        {#if updatePasswordForm}
            <div
                in:slide
                class="grid grid-cols-1 md:grid-cols-2 gap-x-4 max-w-md gap-y-3"
            >
                <div class="">Current password:</div>
                <div>
                    <input
                        type="password"
                        class="input input-sm input-bordered"
                        class:error={old_password === null}
                        bind:value={old_password}
                    />
                </div>
                <div class="">New password:</div>
                <div>
                    <input
                        type="password"
                        class="input input-sm input-bordered"
                        class:error={new_password === null}
                        bind:value={new_password}
                    />
                </div>
                <div class="">New password again:</div>
                <div>
                    <input
                        type="password"
                        class="input input-sm input-bordered"
                        class:error={new_password1 === null}
                        bind:value={new_password1}
                    />
                </div>
            </div>
            <div class="mt-3 flex flex-row gap-x-3">
                <button
                    on:click={() => updatePassword()}
                    class="btn btn-primary btn-xs">Update</button
                >
                <button
                    on:click={() => (updatePasswordForm = false)}
                    class="btn btn-outline btn-xs">Cancel</button
                >
            </div>
        {/if}
    </div>
</div>
