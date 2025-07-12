<script lang="ts">
	import '../auth.css';
	import github from '$lib/images/github.svg';
	import google from '$lib/images/google.svg';
	import { useTranslation } from '$lib/i18n/useTranslation';

	import { token } from '$lib/store';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';

	const { t } = useTranslation();

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
				toast.success($t('auth.signinSuccess'));
				goto('/');
			} else {
				toast.error(data.message || $t('auth.signinFailed'));
			}
		} catch (e) {
			toast.error($t('auth.signinFailed'));
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
	<title>{$t('auth.signin')}</title>
	<meta name="description" content="Fortuna Flow - {$t('auth.signin')}" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>{$t('auth.signin')}</h1>
		<form class="form" on:submit={handleLogin} autocomplete="on">
			<div class="form-field">
				<input type="text" name="username" placeholder={$t('auth.email')} bind:value={username} required />
			</div>
					<div class="form-field">
			<input type="password" name="password" placeholder={$t('auth.password')} bind:value={password} required />
		</div>
		<div class="form-links">
			<a href="/auth/forgot-password">{$t('auth.forgotPassword')}</a>
		</div>
			<div class="form-button">
				<button type="submit" class="glassy-button" disabled={loading}>{loading ? $t('common.loading') : $t('auth.signin')}</button>
			</div>
		</form>
		<div class="optional-sign-in">
			<button class="glassy-light" on:click={loginWithGoogle} type="button">
				<img src={google} alt="Google" class="img-provider" />
				{$t('auth.signinWithGoogle')}
			</button>
			<button class="glassy-light" on:click={loginWithGitHub} type="button">
				<img src={github} alt="GitHub" class="img-provider" />
				{$t('auth.signinWithGitHub')}
			</button>
		</div>
		<div class="auth-links">
			<p>{$t('auth.dontHaveAccount')} <a href="/auth/signup">{$t('auth.signupHere')}</a></p>
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
