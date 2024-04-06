<script lang="ts">
    import Field from "../Field.svelte"
    import { blur } from "svelte/transition"
    let username = ""
    let password = ""
    let passwordValid: boolean = false
    let usernameValid: boolean = false
    let submitting: boolean = false
    let valid = false
    $: {
      valid = usernameValid && passwordValid
    }
    function handleSubmit() {
      submitting = true
      console.log("username:", username)
      console.log("password:", password)
      // TODO: implement login logic here
      setTimeout(() => {
        submitting = false
      }, 1000)
    }
    function handleValidateUsername(val: string) {
      return val?.length > 3
    }
    function handleValidatePassword(val: string) {
      return val?.length > 3
    }
  </script>
  
  <section transition:blur={{ delay: 300, duration: 800 }}>
    <form on:submit|preventDefault={handleSubmit}>
      <h1>Login</h1>
      <Field
        label="Username"
        disabled={submitting}
        bind:value={username}
        bind:valid={usernameValid}
        validate={handleValidateUsername} />
      <Field
        disabled={submitting}
        label="Password"
        bind:value={password}
        type="password"
        bind:valid={passwordValid}
        validate={handleValidatePassword} />
      <p><button type="submit" disabled={!valid || submitting}>Login</button></p>
    </form>
  </section>
  
  <style lang="postcss">
    h1 {
      font-family: sans-serif;
      font-size: 32px;
      color: black;
    }
    section {
      margin: 0 auto;
      width: 300px;
    }
    form {
      margin: 80px 0 0 0;
    }
    button {
      margin-top: 1rem;
      background: rgb(0, 180, 96);
      color: white;
      border-radius: 0.25rem;
      border: 0 none;
      font-size: 18px;
      padding: 0.6rem 1.2rem;
    }
    button:disabled {
      background: #ddd;
    }
  </style>