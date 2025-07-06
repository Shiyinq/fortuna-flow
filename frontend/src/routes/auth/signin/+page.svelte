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

<svelte:head>
	<title>Sign in</title>
	<meta name="description" content="Fortuna Flow - Sign in" />
</svelte:head>

<div class="auth sign-in">
	<form class="form" method="POST" action="?/signIn" use:enhance>
		<h1>Sign in</h1>
		<p>Welcome to Fotuna Flow 🍀</p>
		<div class="form-field">
			<input
				class="default"
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
				class="default"
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
			<button class="nb-button default" type="submit" name="signin">🔑 SIGN IN</button>
		</div>
		<p class="link-auth">
			Don't have an account? <a href="/auth/signup">Sign up</a>
		</p>
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
	</form>
</div>

<style>
	.optional-sign-in {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-top: 16px;
		gap: 12px;
		max-width: none;
		margin-left: 0;
		margin-right: 0;
	}

	.optional-sign-in button {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 0;
		padding: 12px 0;
		width: 100%;
		max-width: none;
		box-sizing: border-box;
		font-size: 1rem;
		font-weight: 600;
		border-radius: 10px;
		height: auto;
		text-transform: uppercase;
		gap: 8px;
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

	.auth {
		min-height: 80vh;
		display: flex;
		justify-content: center;
		align-items: center;
		background: none;
	}

	.form {
		width: 100%;
		max-width: 400px;
		margin: 0 auto;
		padding: 24px 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15), 0 1.5px 4px rgba(44,62,80,0.08);
		color: #222;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.form:hover {
		background: rgba(255,255,255,0.7);
		box-shadow: 0 12px 40px rgba(180, 200, 220, 0.2), 0 2px 8px rgba(44,62,80,0.12);
		transform: translateY(-1px);
	}

	.form h1 {
		margin: 0 0 16px 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
		color: #222;
	}

	.form-button button,
	.nb-button.default {
		width: 100%;
		padding: 12px 0;
		font-size: 1.1rem;
		font-weight: 700;
		color: var(--color-theme-1);
		background: rgba(255,255,255,0.7);
		border: 1.5px solid var(--color-theme-1);
		border-radius: 10px;
		box-shadow: 0 4px 16px rgba(180, 200, 220, 0.10), 0 1px 4px rgba(44,62,80,0.08);
		cursor: pointer;
		transition: background 0.15s, color 0.15s, box-shadow 0.15s;
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
	}

	.form-button button:hover,
	.nb-button.default:hover {
		background: var(--color-theme-1);
		color: #fff;
		box-shadow: 0 6px 24px rgba(0,200,83,0.18), 0 2px 8px rgba(44,62,80,0.12);
	}

	@media (max-width: 600px) {
		.optional-sign-in {
			flex-direction: column;
			gap: 8px;
		}
	}
</style>
