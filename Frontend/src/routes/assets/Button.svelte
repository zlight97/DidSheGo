<script lang="ts">
  import { onMount } from "svelte";
  export let label: string
  export let submitting : boolean = false
  export let handleSubmit: (val: number) => Promise<EpochTimeStamp>
  export let id : number = -1
  export let time: EpochTimeStamp = 123;
  let timeStr: string = "";
  let color : string;
  let hoverColor : string;
  onMount(() =>{
    let interval = setInterval(() => 
    {
      updateColors()
      timeStr = getTime()
    }, 1000)
  })
  function updateColors()
  {
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
  const submitF = async (e: any) => {
    submitting = true
    let tempTime: EpochTimeStamp = await handleSubmit(id)
    if(tempTime)
    {
      time = tempTime > time ? tempTime : time;
      updateColors()
    }
    submitting = false
  }
  
  function getTime()
  {
    let d = new Date(Date.now()-time);
    let dateString = "";
    let days = d.getUTCDate() - 1;
    if(days>0)
      dateString = dateString + days + "d "
    let hours = d.getUTCHours();
    if(hours>0)
      dateString = dateString + hours + "h "
    let minutes = d.getUTCMinutes();
      dateString = dateString + minutes + "m"
    return dateString
  }

</script>
<button style="--button-color: {color}; --button-hover: {hoverColor}"
 on:click|preventDefault={submitF} disabled={submitting}>{label}. Last: {timeStr} ago.</button>

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