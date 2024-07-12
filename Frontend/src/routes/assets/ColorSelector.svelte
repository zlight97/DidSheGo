<script lang="ts">
    import { getContext, onMount } from "svelte";
    import Field from "./Field.svelte";
    import type { Context } from 'svelte-simple-modal';
    import ColorPicker from 'svelte-awesome-color-picker';
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
    let lowColor: string = getStoredStr('lowColor'+storedTag,'#00ff24')
    let midColor: string = getStoredStr('midColor'+storedTag,'#ffc100')
    let highColor: string = getStoredStr('highColor'+storedTag,'#ff0000')
    let valid = false
    $: {
      valid = midValid && highValid
    }

    function getStoredStr(name: string, base: string)
  {
    let tempNum = localStorage.getItem(name)
    if(tempNum === null)
    {
      return base
    }
    return tempNum
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
        localStorage.setItem("lowColor"+storedTag, lowColor)
        localStorage.setItem("midColor"+storedTag, midColor)
        localStorage.setItem("highColor"+storedTag, highColor)
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
    <ColorPicker
	bind:hex={lowColor}
    label="Low Color"
    />
    <ColorPicker
	bind:hex={midColor}
    label="Middle Color"
    />
    <ColorPicker
	bind:hex={highColor}
    label="High Color"
    />
    <Field
    label="Middle start time (Hours)"
    disabled={false}
    bind:value={midValue}
    bind:valid={midValid}
    validate={validateTime} />
    <Field
    label="High start time (Hours)"
    disabled={false}
    bind:value={highValue}
    bind:valid={highValid}
    validate={validateTime} />
    <p><button type="submit" disabled={!valid}>Save</button></p>
</form>