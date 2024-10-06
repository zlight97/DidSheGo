<script lang="ts">
    import { onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { petlistid } from "$lib/stores"
    import Button from "./assets/Button.svelte";
    import PetButton from "./assets/PetButton.svelte";
    import { getPetInfo, submitTime, createNewAction, createNewPet, sendSharePet} from "$lib/api";
    import { logout, updateToken, type PetInfo } from "$lib/index"
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
    let shared = "Share with (email):";
    const modal = writable(null);
    let loaded = false;

    
    const getData = async () => {
      tk = localStorage.getItem('token')
      if(tk)
      {
        const petInfo = await getPetInfo(tk).catch((error) => {
          console.log(error);
          // logout()
      })
        pets = petInfo;
        loaded = true
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
      modal.set(null)
      edit = false
    }

    function goBack(val: number){
      getData();
      selectPet(val);
    }

    function listPets(){
      petlistid.set(selectedPet);
      goto('/list')
    }

    const sharePet = async (email: string) => {
      shared = "..."
      if(!tk)
      {
        logout()
        return 0;
      }
      else if(selectedPet<0)
      {
        goto('/')
      }
      let resp = await sendSharePet(email, tk, selectedPet);
      if(!resp || resp.success > 0)
      {
        if (resp.success > 1)
        {
          shared = "Already Shared"
        }
        else{
          shared = "Share Failed"
        }
        return 0
      }
      shared = "Shared"
    }
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
              lowColor= {getStoredStr('lowColoraID'+v.id,'#00ff24')}
              midColor={getStoredStr('midColoraID'+v.id,'#ffc100')}
              highColor= {getStoredStr('highColoraID'+v.id,'#ff0000')}
              midTime={getStoredInt("maID"+v.id,4)}
              highTime={getStoredInt("haID"+v.id,6)}
            />
          {/if}
        {/each}
        <NewButton 
          handleSubmit={newAction}
        />
        {#if edit}
          <NewButton 
            label={shared}
            handleSubmit={sharePet}
          />
        {/if}
        <PetButton
          label={edit?"Done editing":"Edit"}
          handleSubmit={swapEdit}
        />
        <div class="clear"></div>
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
  .clear { clear: both; height: 60px; }

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