<script lang="ts">
    import Field from "../assets/Field.svelte"
    import { blur } from "svelte/transition"
    import { createAccount, userSignIn } from "$lib/api"
    import { goto } from "$app/navigation"
    import { token } from "$lib/stores"
    import type { Login } from "$lib";
    import { onMount } from "svelte";
    import Header from "../assets/Header.svelte";

    let email = ""
    let password = ""
    let secondPw = ""
    let passwordValid: boolean = false
    let emailValid: boolean = false
    let submitting: boolean = false
    let save: boolean = false
    let newAcc: boolean = false
    let invalidEmail: Set<string> = new Set<string>()
    let valid = false
    $: {
      valid = emailValid && passwordValid
    }

    const setSessionUser = async (sessionUser: Login) => {
      if (sessionUser.success) {
        localStorage.token = sessionUser.token;
        await token.set(sessionUser);
        goto('/');
      }
    };
    
    const checkLogin = async (sessionUser: Login) => {
      if (!sessionUser.success) {
        invalidEmail.add(email)
        handleValidateUsername(email)
      }
      else{
        setSessionUser(sessionUser);
      }
    };

    function checkSavedCreds()
    {
      let em = localStorage.getItem('email')
      let pw = localStorage.getItem('password')
      if(em && pw)
      {
        save = true;
        email = em;
        password = pw;
        emailValid = handleValidateUsername(email)
        passwordValid = handleValidatePassword(password);
      }
    }
    function swapLoginState()
    {
      if(newAcc)
      {
        newAcc = false
        checkSavedCreds()
      }
      else
      {
        newAcc = true
        email = ""
        password = ""
        secondPw = ""
        emailValid = handleValidateUsername(email)
        passwordValid = handleValidatePassword(password);
      }
    }
    onMount(checkSavedCreds)

    const handleSubmit = async () => {
      if(!newAcc)
      {
        if(save)
        {
          localStorage.email = email;
          localStorage.password = password;
        }else{
          localStorage.removeItem("email");
          localStorage.removeItem("password");
        }
        const sessionUser = await userSignIn(email, password).catch((error) => {
          console.log(error);
          return null;
        });

        await setSessionUser(sessionUser);
      }
      else
      {
        const sessionUser = await createAccount(email,password).catch((error)=>{
          console.log(error);
          return null;
        }
        );
        await checkLogin(sessionUser);
      }
	};

    function handleValidateUsername(val: string) {
      if(newAcc)
      {
        return val?.length > 3 && ! (val in invalidEmail) && val.match(".*@.*\..+")
      }
      return val?.length > 3 && val.match(".*@.*\\..+")
    }
    function handleValidatePassword(val: string) {
      if(newAcc)
      {
        return (password===secondPw) && val?.length>3
      }
      return val?.length > 3
    }
  </script>
  <Header/>
  <section transition:blur={{ delay: 300, duration: 800 }}>
    <form on:submit|preventDefault={handleSubmit}>
      {#if newAcc}
      <h1>Create New Account</h1>
      {:else}
      <h1>Login</h1>
      {/if}
      <Field
        label="Email"
        disabled={submitting}
        bind:value={email}
        bind:valid={emailValid}
        validate={handleValidateUsername} />
      <Field
        disabled={submitting}
        label="Password"
        bind:value={password}
        type="password"
        bind:valid={passwordValid}
        validate={handleValidatePassword} />
      {#if newAcc}
      <Field
      disabled={submitting}
      label="Validate Password"
      bind:value={secondPw}
      type="password"
      bind:valid={passwordValid}
      validate={handleValidatePassword} />
      {:else}
      <input type="checkbox" bind:checked={save} />
      Remember me
      {/if}
      <p><button type="submit" disabled={!valid || submitting}>{#if newAcc}Create Account{:else}Login{/if}</button></p>
      
      <a href='#' on:click={swapLoginState}>{#if newAcc}Login{:else}New Account{/if}</a>
      
      
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