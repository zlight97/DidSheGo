<script lang="ts">
  export let color: string = 'black';
  export let hoverColor: string = 'red';
  export let textColor: string = 'white';
  export let handleSubmit: (val: string) => void
  let state = false;
  let label: string = "Add new";
  let value: string = "";

  function clicked()
  {
    state = true;
  }

  function entered()
  {
    state = false;
    handleSubmit(value)
  }


  function onKeyDown(e: KeyboardEvent) {
    if(state)
		 switch(e.keyCode) { //TODO use an undepricated version of this
      case 13:
        state=false
        if(value!="")
        {
          entered();
        }
        break;
      case 27:
        value = ""
        state=false
        break;
		 }
	}
</script>

{#if !state}
<button style="--button-color: {color}; --button-hover: {hoverColor}; --text-color: {textColor};"
 on:click|preventDefault={clicked} disabled={state}>{label}</button>
 {:else}
<input style="--button-color: {color}; --button-hover: {hoverColor}; --text-color: {textColor};" bind:value={value}/>
 {/if}

<style lang="postcss">
  input {
      margin-top: 1rem;
      background: var(--button-color);
      color: var(--text-color);
      border-radius: 0.25rem;
      border: 0 none;
      font-size: 18px;
      padding: 0.6rem 1.2rem;
    }
  input:hover{
      background: var(--button-hover);
  }
  button {
      margin-top: 1rem;
      background: var(--button-color);
      color: var(--text-color);
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

<svelte:window on:keydown={onKeyDown} />