import { readable, writable } from 'svelte/store';


export const selected_component = writable('')
export const selected_dashboard_component = writable('')


// profile data
export const profile = writable();
export const first_name = writable('');
export const logo = writable('');
export const is_guest = writable(false);
export const first_login = writable(false);
export const email = writable('');

//device
export const boiler_id = writable();

//messenger
export const messenger = writable(false);
export const message = writable('');