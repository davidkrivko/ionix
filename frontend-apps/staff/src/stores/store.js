import { readable, writable } from 'svelte/store';


export const selected_component = writable('')
export const selected_dashboard_component = writable('')

export const reload_trigger = writable(false);
export const mobile_menu = writable(false);
// profile data
export const profile = writable();
export const first_name = writable('');
export const logo = writable('');
export const email = writable();

export const messenger = writable(false);
export const message = writable('');