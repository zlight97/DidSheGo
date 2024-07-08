<script lang="ts">
    import { getContext, onMount } from "svelte";
    import PetButton from "./PetButton.svelte";
    import Field from "./Field.svelte";
    import type { Context } from 'svelte-simple-modal';
    const { close } = getContext<Context>('simple-modal');

    export let actionId = 1;
    export let callback: () => void
    let midValue: string = "";
    let highValue: string = "";
    let storedTag = "aID"+actionId;
    let midValid: boolean = false;
    let highValid: boolean = false;
    let midTime = localStorage.getItem("m"+storedTag)
    let highTime = localStorage.getItem("h"+storedTag)
    let valid = false
    $: {
      valid = midValid && highValid
    }

    onMount(()=>{
        if(midTime!=null){
            midValue = midTime;
            midValid = validateTime(midValue)
        }
        if(highTime!=null)
        {
            highValue = highTime;
            highValid = validateTime(highValue)
        }
    })
    function updateStores()
    {
        localStorage.setItem("m"+storedTag,midValue)
        localStorage.setItem("h"+storedTag,highValue)
        callback()
        close()
    }
    function validateTime(time: string)
    {
        //Must be a number and must exist
        return !!time.match("^[0-9]+$")
    }
  </script>

<form on:submit|preventDefault={updateStores}>
    <Field
    label="Yellow start time (Hours)"
    disabled={false}
    bind:value={midValue}
    bind:valid={midValid}
    validate={validateTime} />
    <Field
    label="Red start time (Hours)"
    disabled={false}
    bind:value={highValue}
    bind:valid={highValid}
    validate={validateTime} />
    <p><button type="submit" disabled={!valid}>Save</button></p>
</form>