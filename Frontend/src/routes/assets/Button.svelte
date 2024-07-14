<script lang="ts">
  import { shadeColor } from "$lib";
  import { onMount } from "svelte";
  export let label: string
  export let submitting : boolean = false
  export let handleSubmit: (val: number) => Promise<EpochTimeStamp|null> 
  export let id : number = -1
  export let time: EpochTimeStamp = 123;
  export let midTime: number = 4;
  export let highTime: number = 6;
  export let lowColor: string = '#00ff24'
  export let midColor: string = '#ffc100'
  export let highColor: string = '#ff0000'
  let calcTime: EpochTimeStamp = 123;
  let interval: number | null = null;
  let timeStr: string = "";
  let color : string;
  let hoverColor : string;
  onMount(() =>{
    calcTime = time*1000
    timeStr = getTime()
    updateColors()
    if(interval===null)
      interval = setInterval(() => 
      {
        updateColors()
        timeStr = getTime()
      }, 10000)
  })


  function updateColors()
  {
    let mt = 3600000 * midTime
    let ht = 3600000 * highTime
    let d = Date.now()
    if(calcTime > d-mt)
    {
      color = lowColor;
    }
    else if(calcTime > d-ht)
    {
      color = midColor;
    }
    else{
      color = highColor
    }
    hoverColor = shadeColor(color,-50)
  }
  const submitF = async (e: any) => {
    submitting = true
    let tempTime: EpochTimeStamp | null = await handleSubmit(id)
    if(tempTime!=null)
    {
      time = tempTime > calcTime ? Math.floor(tempTime/1000) : time;
      timeStr = getTime()
      updateColors()
    }
    submitting = false
  }
  
  function getTime()
  { 
    calcTime = time*1000
    let n = Date.now()
    let d = new Date(n-calcTime);
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