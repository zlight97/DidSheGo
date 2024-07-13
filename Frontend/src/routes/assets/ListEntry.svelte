<script lang="ts">
  import { onMount } from "svelte";
  import { type ActionEntry } from "$lib/index"
  import { deleteOrRestoreAction } from "$lib/api/index"
  export let entry: ActionEntry
  let time: string;
  let buttonLabel: string;
  let color : string;
  let hoverColor : string;
  let tk: string | null;
  onMount(parseEntry)
  function parseEntry()
  {
    let d: Date;
    d = new Date(0)
    d.setUTCSeconds(entry.time)
    time = d.toString()
    time = time.substring(3,time.indexOf(" GMT"))
    tk = localStorage.getItem('token')

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
<div>{entry.name} on {time}<button style="--button-color: {color}; --button-hover: {hoverColor}"
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