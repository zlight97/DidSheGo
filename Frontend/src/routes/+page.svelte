<script lang="ts">
    import { onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { token } from "$lib/stores"
    import Button from "./assets/Button.svelte";
    import PetButton from "./assets/PetButton.svelte";
    import { getPetInfo } from "$lib/api";
    import { logout } from "$lib/index"

    let submitting: boolean = false
    let tk : string | null;
    let pets : Object | null = null;
    let selectedPet = -1;

    onMount(async () => {
      tk = localStorage.getItem('token')
      if(tk)
      {
        const petInfo = await getPetInfo(tk).catch((error) => {
          console.log(error);
          logout()
          return null;
      })
        pets = petInfo;
        console.log(petInfo)
        if(!pets){
          logout()
        }
      }
      else
      {
        logout()
      }
    });
    

    function submitAction(val: number) {
      console.log(token)
      return Date.now()
    }

    function selectPet(val: number) {
      selectedPet = val;
    }

  </script>
  
  <section transition:blur={{ delay: 300, duration: 800 }}>

    {#if pets}
      {#if selectedPet < 0}
          {#each Object.entries(pets) as [key,value]}
            <PetButton
            id={key}
            label={value[0]}
            submitting={submitting}
            handleSubmit={selectPet}
          />
          {/each}
      {:else}
        {#each pets[selectedPet][1] as v}
          <Button
            id={v.id}
            label={v.name}
            submitting={submitting}
            time={v.time}
            handleSubmit={submitAction}
          />
        {/each}
        <PetButton
          id=-1
          label="↩"
          handleSubmit={selectPet}
        />
        <PetButton
          id=-1
          label="Logout"
          handleSubmit={logout}
        />
        
      {/if}
    {:else}
      loading
    {/if}
  </section>
  
  <style lang="postcss">
    section {
      margin: 0 auto;
      width: 300px;
      display:grid
    }
  </style>