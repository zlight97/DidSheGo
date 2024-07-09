import { writable } from 'svelte/store';
export const token = writable();
export const petid = writable();
export const petlistid = writable(-1);

function getStoredStr(name: string, base: string)
{
  let tempNum = localStorage.getItem(name)
  if(tempNum === null)
  {
    return base
  }
  return tempNum
}