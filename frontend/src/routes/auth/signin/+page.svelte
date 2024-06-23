<script lang="ts">
	import '../auth.css';
	import github from '$lib/images/github.svg';
	import google from '$lib/images/google.svg';

	import { token } from '$lib/store';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';

	export let form: any;

	let username = '';
	let password = '';

	const clearValidation = (key: string) => {
		delete form?.errors[key];
	};

	$: if (form) {
		if (form?.status) {
			toast.success(form?.message);
			token.set(form?.access_token);
			goto('/');
		} else {
			toast.error(form?.message);
		}
	}

	const loginWithGitHub = () => {
		window.location.href = `${FORTUNA_API_BASE_URL}/auth/github/signin`;
	};
	const loginWithGoogle = () => {
		window.location.href = `${FORTUNA_API_BASE_URL}/auth/google/signin`;
	};
</script>

<Toaster richColors position="top-center" />
<div class="auth sign-in">
	<form class="form" method="POST" action="?/signIn" use:enhance>
		<h1>Sign in</h1>
		<p>Welcome to Fotuna Flow</p>
		<div class="form-field">
			<input
				class="nb-input default"
				type="text"
				name="username"
				id="username"
				placeholder="Username"
				bind:value={username}
				on:keydown={() => clearValidation('username')}
			/>
			{#if form?.errors?.username}
				<span>{form?.errors?.username}</span>
			{/if}
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="password"
				name="password"
				id="password"
				placeholder="Password"
				bind:value={password}
				on:keydown={() => clearValidation('password')}
			/>
			{#if form?.errors?.password}
				<span>{form?.errors?.password}</span>
			{/if}
		</div>
		<div class="form-button">
			<button class="nb-button default" type="submit" name="signin">Sign in</button>
		</div>
		<p class="link-auth">
			Don't have an account? <a href="/auth/signup">Sign up</a>
		</p>
	</form>

	<div class="optional-sign-in">
		<button class="nb-button default" name="github" on:click={loginWithGitHub}>
			<img src={github} alt="GitHub" />
			Sign in with GitHub
		</button>
		<button class="nb-button default" name="signin" on:click={loginWithGoogle}>
			<img class="img-google" src={google} alt="Google" />
			Sign in with Google
		</button>
	</div>
</div>

<style>
	.optional-sign-in {
		width: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-top: 16px;
	}

	.optional-sign-in button {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 8px;
		padding: 8px;
		width: 100%;
		box-sizing: border-box;
	}

	.optional-sign-in img {
		width: 2em;
		height: 2em;
		object-fit: contain;
		margin-right: 8px;
	}

	.img-google {
		width: 1.5em !important;
		height: 1.5em !important;
	}
</style>
