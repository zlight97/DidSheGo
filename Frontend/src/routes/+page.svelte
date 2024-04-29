<script lang="ts">
    import { onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { token } from "$lib/stores"
    import Button from "./assets/Button.svelte";
    import PetButton from "./assets/PetButton.svelte";
    import { getPetInfo, submitTime, createNewAction} from "$lib/api";
    import { logout, updateToken } from "$lib/index"
    import Spinner from "./assets/Spinner.svelte";
    import { goto } from "$app/navigation";
    import NewButton from "./assets/NewButton.svelte";

    let submitting: boolean = false
    let tk : string | null;
    let pets : Object | null = null;
    let selectedPet = -1;
    let selectedTime: EpochTimeStamp | null = null;

    
    const getData = async () => {
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
    }

    onMount(getData);
    
    const submitAction = async (actionId: number) => {
      if(!tk)
      {
        logout()
        return 0;
      }
      let resp = await submitTime(tk,actionId,selectedTime?selectedTime:Date.now())
      if(!resp || !resp.success)
        return 0;
      tk = updateToken(resp.token)
      return selectedTime?selectedTime:Date.now()
    }

    const newAction = async (newAction: string) => {
      if(!tk)
      {
        logout()
        return 0;
      }
      let resp = await createNewAction(newAction,selectedPet, tk);
      if(!resp || !resp.success)
        return 0
      getData();
    }

    function selectPet(val: number) {
      selectedPet = val;
    }

    function goBack(val: number){
      getData();
      selectPet(val);
    }

</script>
  
  <section transition:blur={{ delay: 300, duration: 800 }}>

    {#if pets}
      {#if selectedPet < 0}
          {#each Object.entries(pets) as [key,value]}
            <PetButton
            id={Number(key)}
            label={value[0]}
            submitting={submitting}
            handleSubmit={selectPet}
          />
          {/each}

          <footer style="margin-left: 6%">
          <PetButton
          id=-1
          label="Logout"
          handleSubmit={logout}
          />

          </footer>
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
        <NewButton 
          handleSubmit={newAction}
        />
        <footer>
        <PetButton
          id=-1
          label="↩"
          handleSubmit={goBack}
        />
        <PetButton
          id=-1
          label="Logout"
          handleSubmit={logout}
        />
      </footer>
      {/if}
    {:else}
      <Spinner />
    {/if}
  </section>
  
  <style lang="postcss">
    section {
      margin: 0 auto;
      width: 300px;
      display:grid
    }
    footer {
      position:absolute;
      bottom:0;
      width:100%;
      height:60px;
      max-width: fit-content;
      margin-left: auto;
      margin-right: auto;
  }
  </style>