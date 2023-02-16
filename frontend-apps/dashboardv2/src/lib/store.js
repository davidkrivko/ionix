import { writable } from "svelte/store";


export const selected_component = writable(0);

export const first_name = writable(0);
export const last_name = writable(0);
export const email = writable();