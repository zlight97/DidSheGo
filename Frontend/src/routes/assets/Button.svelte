<script lang="ts">
  import { shadeColor } from "$lib";
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
    timeStr = getTime()
    updateColors()
    let interval = setInterval(() => 
    {
      updateColors()
      timeStr = getTime()
    }, 1000)
  })


  function getStoredStr(name: string, base: string)
  {
    let tempNum = localStorage.getItem(name)
    if(tempNum === null)
    {
      return base
    }
    return tempNum
  }

  function getStoredInt(name: string, base: number)
  {
    let tempNum = localStorage.getItem(name)
    if(tempNum === null)
    {
      return base
    }
    return parseInt(tempNum)
  }

  function updateColors()
  {
    let midTime: number = getStoredInt('midTime',14400000)
    let highTime: number = getStoredInt('highTime',21600000)
    let lowColor: string = getStoredStr('lowColor','#00ff24')
    let midColor: string = getStoredStr('midColor','#ffc100')
    let highColor: string = getStoredStr('highColor','#ff0000')
    let d = Date.now()
    if(time > d-midTime)
    {
      color = lowColor;
    }
    else if(time > d-highTime)
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