<script lang="ts">
	import '../auth.css';
	import { enhance } from '$app/forms';
	import { Toaster, toast } from 'svelte-sonner';

	export let form: any;

	let name = '';
	let username = '';
	let email = '';
	let password = '';
	let confirmPassword = '';

	const clearValidation = (key: string) => {
		delete form?.errors[key];
	};

	$: if (form) {
		if (form?.status) {
			toast.success(form?.message);
		} else {
			toast.error(form?.message);
		}
	}
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>Sign up</title>
	<meta name="description" content="Fortuna Flow - Sign up" />
</svelte:head>

<div class="auth sign-in">
	<form class="form" method="POST" action="?/signUp" use:enhance>
		<h1>Sign up</h1>
		<p>Create an account before sign in</p>
		<div class="form-field">
			<input
				class="default"
				type="text"
				name="name"
				id="name"
				placeholder="Enter your name"
				bind:value={name}
				on:keydown={() => clearValidation('name')}
			/>
			{#if form?.errors?.name}
				<span>{form?.errors?.name}</span>
			{/if}
		</div>
		<div class="form-field">
			<input
				class="default"
				type="text"
				name="username"
				id="username"
				placeholder="Enter your username"
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
				type="email"
				name="email"
				id="email"
				placeholder="Enter your email"
				bind:value={email}
				on:keydown={() => clearValidation('email')}
			/>
			{#if form?.errors?.email}
				<span>{form?.errors?.email}</span>
			{/if}
		</div>
		<div class="form-field">
			<input
				class="default"
				type="password"
				name="password"
				id="password"
				placeholder="Enter your password"
				bind:value={password}
				on:keydown={() => clearValidation('password')}
			/>
			{#if form?.errors?.password}
				<span>{form?.errors?.password}</span>
			{/if}
		</div>
		<div class="form-field">
			<input
				class="default"
				type="password"
				name="confirmPassword"
				id="confirmPassword"
				placeholder="Re enter your password"
				bind:value={confirmPassword}
				on:keydown={() => clearValidation('confirmPassword')}
			/>
			{#if form?.errors?.confirmPassword}
				<span>{form?.errors?.confirmPassword}</span>
			{/if}
		</div>
		<div class="form-button">
			<button class="nb-button default" type="submit" name="signup">📝 SIGN UP</button>
		</div>
		<p class="link-auth">
			Already have an account? <a href="/auth/signin">Sign in</a>
		</p>
	</form>
</div>

<style>
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
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		color: #222;
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
		box-shadow: 0 4px 16px rgba(180, 200, 220, 0.10);
		cursor: pointer;
		transition: background 0.15s, color 0.15s, box-shadow 0.15s;
		backdrop-filter: blur(6px);
	}

	.form-button button:hover,
	.nb-button.default:hover {
		background: var(--color-theme-1);
		color: #fff;
		box-shadow: 0 6px 24px rgba(0,200,83,0.18);
	}
</style>
