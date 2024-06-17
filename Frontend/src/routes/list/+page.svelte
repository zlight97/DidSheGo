<script lang="ts">
    import { onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { petlistid } from "$lib/stores"
    import PetButton from "../assets/PetButton.svelte";
    import { getPetList } from "$lib/api";
    import { logout, type ActionEntry} from "$lib/index"
    import Spinner from "../assets/Spinner.svelte";
    import { goto } from "$app/navigation";
    import ListEntry from "../assets/ListEntry.svelte";

    let tk : string | null;
    let pets : Array<ActionEntry> | null = null;
    let petid : number;

    petlistid.subscribe((value: number) => {
		  petid = value;
	  });

    const getData = async () => {
      tk = localStorage.getItem('token')
      if(tk && petid >=0)
      {
        const petInfo = await getPetList(tk, petid).catch((error) => {
          console.log(error);
          goto('/')
          return null;
      })
        pets = petInfo;
        console.log(petInfo)
        if(!pets){
          goto('/')
        }
      }
      else
      {
        goto('/')
      }
    }

    function goBack(){
      goto('/')
    }

    onMount(getData);

</script>
  

{#if pets}
  <section transition:blur={{ delay: 300, duration: 800 }}>
      {#each pets as entry}
        <ListEntry
          entry={entry}
        />
      {/each}
      <footer>
        <PetButton
          label="↩"
          handleSubmit={goBack}
        />
        <PetButton
          label="Logout"
          handleSubmit={logout}
        />
      </footer>
  </section>
{:else}
    <Spinner />
{/if}
  
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