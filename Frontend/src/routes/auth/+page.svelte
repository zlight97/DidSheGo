<script lang="ts">
    import Field from "../assets/Field.svelte"
    import { blur } from "svelte/transition"
    import { userSignIn } from "$lib/api"

    let email = ""
    let password = ""
    let passwordValid: boolean = false
    let emailValid: boolean = false
    let submitting: boolean = false
    let valid = false
    $: {
      valid = emailValid && passwordValid
    }

    const setSessionUser = async (sessionUser) => {
      if (sessionUser.success) {
        console.log(sessionUser);
        console.log(`You're now logged in.`);
        localStorage.token = sessionUser.token;
        // await user.set(sessionUser);
        // goto('/');
      }
    };

    // function handleSubmit() {
    //   submitting = true
    //   console.log("username:", username)
    //   console.log("password:", password)
    //   // TODO: implement login logic here
    //   setTimeout(() => {
    //     submitting = false
    //   }, 1000)
    // }

    const handleSubmit = async () => {
		const sessionUser = await userSignIn(email, password).catch((error) => {
			console.log(error);
			return null;
		});

		await setSessionUser(sessionUser);
	};

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