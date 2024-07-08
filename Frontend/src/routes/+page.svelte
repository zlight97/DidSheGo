<script lang="ts">
    import { SvelteComponent, getContext, onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { petlistid } from "$lib/stores"
    import Button from "./assets/Button.svelte";
    import PetButton from "./assets/PetButton.svelte";
    import { getPetInfo, submitTime, createNewAction, createNewPet} from "$lib/api";
    import { logout, updateToken, type NumberDataTuple, type PetInfo } from "$lib/index"
    import Spinner from "./assets/Spinner.svelte";
    import { goto } from "$app/navigation";
    import NewButton from "./assets/NewButton.svelte";
    import Header from "./assets/Header.svelte";
    import { Modal, bind } from "svelte-simple-modal";
    import ColorSelector from "./assets/ColorSelector.svelte";
    import { writable } from "svelte/store";

    let submitting: boolean = false
    let tk : string | null;
    let pets : PetInfo | null = null;
    let selectedPet: number = -1;
    let selectedTime: EpochTimeStamp | null = null;
    let edit: boolean = false;
    const modal = writable(null);

    
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
        if(!pets){
          logout()
        }
      }
      else
      {
        logout()
      }
    }

    onMount(() => {
      getData();
      let interval = setInterval(() => 
    {
       getData();
    }, 400000)
    });

    function colorSelectorCallback()
    {
      getData()
    }

    function swapEdit()
    {
      edit = !edit;
    }

    const handleButton = async (actionId: number) =>{
      if(edit)
      {
        //module doesnt seem to be meant for typescript, so we have to ignore this error
        // @ts-ignore
        modal.set(bind(ColorSelector, {actionId: actionId, callback: colorSelectorCallback}));
        return null;
      }
      else
      {
        return submitAction(actionId);
      }
    }
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

    const newPet = async (newPet: string) => {
      if(!tk)
      {
        logout()
        return 0;
      }
      let resp = await createNewPet(newPet, tk);
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

    function listPets(){
      petlistid.set(selectedPet);
      goto('/list')
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

</script>
  <Header/>
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
        <NewButton 
        handleSubmit={newPet}
        />

          <footer style="margin-left: 6%">
          <PetButton
          label="Logout"
          handleSubmit={logout}
          />

          </footer>
      {:else}
      <Modal show={$modal}></Modal>
        {#each pets[selectedPet][1] as v}
          {#if v.id >= 0}
            <Button
              id={v.id}
              label={v.name}
              submitting={submitting}
              time={v.time}
              handleSubmit={handleButton}
              midTime={getStoredInt("maID"+v.id,4)}
              highTime={getStoredInt("haID"+v.id,6)}
            />
          {/if}
        {/each}
        <NewButton 
          handleSubmit={newAction}
        />
        <PetButton
          label={edit?"Done editing":"Edit"}
          handleSubmit={swapEdit}
        />
        <footer>
        <PetButton
          label="↩"
          handleSubmit={goBack}
        />
        <PetButton
          label="Logout"
          handleSubmit={logout}
        />
        <PetButton
          label="View All"
          handleSubmit={listPets}
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
      position:fixed;
      bottom:0;
      width:100%;
      height:60px;
      max-width: fit-content;
      margin-left: auto;
      margin-right: auto;
  }
  </style>