<script lang="ts">
  import { onMount } from "svelte";
  import { type ActionEntry } from "$lib/index"
  import { deleteOrRestoreAction } from "$lib/api/index"
    import { parse } from "svelte/compiler";
  export let entry: ActionEntry
  let buttonLabel: string;
  let color : string;
  let hoverColor : string;
  let tk: string | null;
  onMount(parseEntry)
  function parseEntry()
  {
    tk = localStorage.getItem('token')

    console.log(entry.time)
    if(entry.deleted){
      buttonLabel = 'Recover'
      color = '#00b460';
      hoverColor = '#006400';
    }
    else{
      buttonLabel = 'Delete'
      color = 'red'
      hoverColor = 'black'
    }
  }
  const handleSubmit = async () => {
      if(!tk)
      {
        return 0;
      }
      entry.deleted = ! entry.deleted;
      parseEntry()
      let resp = await deleteOrRestoreAction(entry.actionid, tk);
      if(!resp || !resp.success)
        return 0;
    }
  function submitF(e: any) {
    handleSubmit()
  }
</script>
<div>{entry.name} at {entry.time.toString().substring(0,19)}<button style="--button-color: {color}; --button-hover: {hoverColor}"
 on:click|preventDefault={submitF} >{buttonLabel}</button>
</div>

<style lang="postcss">
  button {
      margin-top: 1rem;
      background: var(--button-color);
      color: white;
      border-radius: 0.25rem;
      border: 0 none;
      font-size: 18px;
      padding: 0.6rem 1.2rem;
    }
  button:hover{
      background: var(--button-hover);
  }
  button:disabled {
    background: #ddd;
  }
</style>