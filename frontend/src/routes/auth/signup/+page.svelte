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
		console.log(form);
	}
</script>

<Toaster richColors position="top-center" />
<div class="auth sign-in">
	<form class="form" method="POST" action="/auth?/signUp" use:enhance>
		<h1>Sign up</h1>
		<p>Create an account before sign in</p>
		<div class="form-field">
			<input
				class="nb-input default"
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
				class="nb-input default"
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
				class="nb-input default"
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
				class="nb-input default"
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
				class="nb-input default"
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
			<button class="nb-button default" type="submit" name="signup">Sign up</button>
		</div>
		<p class="link-auth">
			Already have an account? <a href="/auth/signin">Sign in</a>
		</p>
	</form>
</div>

<style>
	.auth {
		height: 80vh;
		display: flex;
		justify-content: center;
	}
</style>
