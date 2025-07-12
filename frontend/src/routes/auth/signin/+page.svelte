<script lang="ts">
	import '../auth.css';
	import github from '$lib/images/github.svg';
	import google from '$lib/images/google.svg';

	import { token } from '$lib/store';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';

	let username = '';
	let password = '';
	let loading = false;

	const handleLogin = async (event: Event) => {
		event.preventDefault();
		loading = true;
		try {
			const response = await fetch(`${FORTUNA_API_BASE_URL}/auth/signin`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
				credentials: 'include',
				body: new URLSearchParams({ username, password }).toString()
			});
			const data = await response.json();
			if (response.ok && data.access_token) {
				token.set(data.access_token);
				toast.success('Sign in successful!');
				goto('/');
			} else {
				toast.error(data.message || 'Sign in failed.');
			}
		} catch (e) {
			toast.error('Sign in failed.');
		} finally {
			loading = false;
		}
	};

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

<div class="auth">
	<div class="form glassy">
		<h1>Sign In</h1>
		<form class="form" on:submit={handleLogin} autocomplete="on">
			<div class="form-field">
				<input type="text" name="username" placeholder="Username" bind:value={username} required />
			</div>
					<div class="form-field">
			<input type="password" name="password" placeholder="Password" bind:value={password} required />
		</div>
		<div class="form-links">
			<a href="/auth/forgot-password">Forgot Password?</a>
		</div>
			<div class="form-button">
				<button type="submit" class="glassy-button" disabled={loading}>{loading ? 'Signing in...' : 'Sign In'}</button>
			</div>
		</form>
		<div class="optional-sign-in">
			<button class="glassy-light" on:click={loginWithGoogle} type="button">
				<img src={google} alt="Google" class="img-provider" />
				Sign in with Google
			</button>
			<button class="glassy-light" on:click={loginWithGitHub} type="button">
				<img src={github} alt="GitHub" class="img-provider" />
				Sign in with GitHub
			</button>
		</div>
		<div class="auth-links">
			<p>Don't have an account? <a href="/auth/signup">Sign up</a></p>
		</div>
	</div>
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

	.img-provider {
		width: 1.7em;
		height: 1.7em;
		object-fit: contain;
		margin-right: 8px;
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
		color: var(--color-text-strong);
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



	@media (max-width: 600px) {
		.optional-sign-in {
			flex-direction: column;
			gap: 8px;
		}
	}
</style>
