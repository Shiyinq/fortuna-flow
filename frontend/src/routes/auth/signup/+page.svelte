<script lang="ts">
	import '../auth.css';
	import { enhance } from '$app/forms';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();

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
	<title>{$t('auth.signup')}</title>
	<meta name="description" content="Fortuna Flow - {$t('auth.signup')}" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>{$t('auth.signup')}</h1>
		<form method="POST" action="?/signUp" use:enhance class="form">
			<div class="form-field">
				<input type="text" name="name" placeholder={$t('profile.fullName')} required />
			</div>
			<div class="form-field">
				<input type="text" name="username" placeholder={$t('auth.username')} required />
			</div>
			<div class="form-field">
				<input type="email" name="email" placeholder={$t('auth.email')} required />
			</div>
			<div class="form-field">
				<input type="password" name="password" placeholder={$t('auth.password')} required />
			</div>
			<div class="form-field">
				<input type="password" name="confirmPassword" placeholder={$t('auth.confirmPassword')} required />
			</div>
			<div class="form-button">
				<button type="submit" name="signUp" class="glassy-button">{$t('auth.signup')}</button>
			</div>
		</form>
		<div class="auth-links">
			<p>{$t('auth.alreadyHaveAccount')} <a href="/auth/signin">{$t('auth.signinHere')}</a></p>
			<p>{$t('auth.noVerificationEmail')} <a href="/auth/send-verification">{$t('auth.resend')}</a></p>
		</div>
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
</style>
