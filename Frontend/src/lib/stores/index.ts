import { writable } from 'svelte/store';
export const token = writable();
export const petid = writable();
export const petlistid = writable(-1);