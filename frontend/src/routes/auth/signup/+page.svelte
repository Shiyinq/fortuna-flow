<script lang="ts">
	import '../auth.css';
	import { enhance } from '$app/forms';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';

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

	const loginWithGitHub = () => {
		window.location.href = `${FORTUNA_API_BASE_URL}/auth/github/signin`;
	};
	const loginWithGoogle = () => {
		window.location.href = `${FORTUNA_API_BASE_URL}/auth/google/signin`;
	};
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>Sign up</title>
	<meta name="description" content="Fortuna Flow - Sign up" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>Sign Up</h1>
		<form method="POST" action="?/signUp" use:enhance class="form">
			<div class="form-field">
				<input type="text" name="name" placeholder="Name" required />
			</div>
			<div class="form-field">
				<input type="text" name="username" placeholder="Username" required />
			</div>
			<div class="form-field">
				<input type="email" name="email" placeholder="Email" required />
			</div>
			<div class="form-field">
				<input type="password" name="password" placeholder="Password" required />
			</div>
			<div class="form-field">
				<input type="password" name="confirmPassword" placeholder="Confirm Password" required />
			</div>
			<div class="form-button">
				<button type="submit" name="signUp" class="glassy-button">Sign Up</button>
			</div>
		</form>
		<p>
			Already have an account? <a href="/auth/signin">Sign in</a>
		</p>
	</div>
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
		color: #222;
	}

	.form h1 {
		margin: 0 0 16px 0;
	}

	.form-button button {
		width: 100%;
		padding: 12px 0;
		font-size: 1.1rem;
		font-weight: 700;
		color: var(--color-theme-1);
		border-radius: 10px;
		cursor: pointer;
	}
</style>
