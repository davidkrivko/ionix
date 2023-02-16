import { readable, writable } from 'svelte/store';


export const selected_dashboard_component = writable('properties');

// scheduling page
export const selected_thermostat = writable(4);

export const reload_trigger = writable(false);
export const mobile_menu = writable(false);
// profile data
export const profile = writable();
export const first_name = writable('');
export const logo = writable('');
export const email = writable();

//properties
export const selected_building = writable();

// configuration and boiler data
export const boiler_id = writable();
export const outdoor_temp = writable();
export const wwsd_setpoint = writable();

//popups
export const qcodepopup = writable(false);
export const confirm_popup = writable(false);
export const messenger = writable(false);
export const message = writable('');