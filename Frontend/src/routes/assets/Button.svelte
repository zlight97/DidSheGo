<script lang="ts">
  import { onMount } from "svelte";
  export let label: string
  export let submitting : boolean = false
  export let handleSubmit: (val: number) => EpochTimeStamp
  export let id : number = -1
  export let time: EpochTimeStamp = 123;
  let color : string;
  let hoverColor : string;
  onMount(updateColors)
  function updateColors()
  {
    console.log(time)
    if(time > Date.now()-3600000)
    {
      color = '#00b460';
      hoverColor = '#006400';
    }
    else{
      color = 'black'
      hoverColor = 'red'
    }
  }
  function submitF(e) {
    submitting = true
    console.log(id)
    let tempTime: EpochTimeStamp = handleSubmit(id)
    if(tempTime)
    {
      time = tempTime > time ? tempTime : time;
      updateColors()
    }
    submitting = false
  }
</script>
<button style="--button-color: {color}; --button-hover: {hoverColor}"
 on:click|preventDefault={submitF} disabled={submitting}>{label}</button>

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