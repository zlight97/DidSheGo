<script lang="ts">
    import { onMount } from "svelte";
    import { blur } from "svelte/transition"
    import { goto } from "$app/navigation"
    import { token } from "$lib/stores"
    import Button from "./assets/Button.svelte";

    let submitting: boolean = false
    let valid = false
    let tk = token
    let id = 1

    onMount(async () => {
      fetch("")
      .then(response => response.json())
      .then(data => {
        console.log(data);
        // apiData.set(data);
      }).catch(error => {
        console.log(error);
        return [];
      });
    });

    function submitAction(val: number) {
      console.log(token)
      return Date.now()
    }

  </script>
  
  <section transition:blur={{ delay: 300, duration: 800 }}>
    <form>
      <Button
        label="pee"
        submitting={submitting}
        handleSubmit={submitAction}
        id={id}
      />
    </form>
  </section>
  
  <style lang="postcss">
    section {
      margin: 0 auto;
      width: 300px;
    }
  </style>