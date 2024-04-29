<script lang="ts">
  let color: string = 'black';
  let hoverColor: string = 'red';
  let state = false;
  let label: string = "Add new";
  let value: string = "";
  let submittedValue : string = "";

  function clicked()
  {
    state = true;
  }

  function entered()
  {
    submittedValue = value;
    console.log(value) 
    state = false;
  }

  const handleInput = async (e) =>{
    value = e.target.value
    console.log(value)
    // state = false
  }
</script>

{#if !state}
<button style="--button-color: {color}; --button-hover: {hoverColor}"
 on:click|preventDefault={clicked} disabled={state}>{label}</button>
 {:else}
 <form on:submit|preventDefault={entered}><input bind:value={value} on:input={handleInput} /></form>
 {/if}

<style lang="postcss">
  input {
      margin-top: 1rem;
      background: black;
      color: white;
      border-radius: 0.25rem;
      border: 0 none;
      font-size: 18px;
      padding: 0.6rem 1.2rem;
    }
  input:hover{
      background: red;
  }
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