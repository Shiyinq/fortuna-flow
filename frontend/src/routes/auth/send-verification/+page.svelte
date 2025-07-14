<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { sendVerificationEmail } from '$lib/apis/auth';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();

	let email = '';
	let loading = false;
	let submitted = false;
	let status: 'idle' | 'success' | 'error' = 'idle';
	let errorMessage = '';
	let redirectCountdown = 10;
	let redirectTimer: ReturnType<typeof setInterval> | null = null;

	const handleSendVerification = async (event: Event) => {
		event.preventDefault();
		
		// Basic email validation
		if (!email || !email.includes('@')) {
			toast.error($t('auth.invalidEmail'));
			return;
		}
		
		loading = true;
		try {
			const data = await sendVerificationEmail(email);
			toast.success(data.message || $t('auth.verificationSent'));
			submitted = true;
			status = 'success';
			email = '';
			startRedirectCountdown();
		} catch (error: any) {
			console.error('Send verification error:', error);
			status = 'error';
			if (error.detail) {
				errorMessage = error.detail;
			} else if (error.message) {
				errorMessage = error.message;
			} else if (typeof error === 'string') {
				errorMessage = error;
			} else {
				errorMessage = $t('auth.failedToSendVerification');
			}
			toast.error(errorMessage);
		} finally {
			loading = false;
		}
	};

	function startRedirectCountdown() {
		redirectCountdown = 10;
		if (redirectTimer) clearInterval(redirectTimer);
		redirectTimer = setInterval(() => {
			redirectCountdown--;
			if (redirectCountdown <= 0) {
				clearInterval(redirectTimer!);
				goto('/auth/signin');
			}
		}, 1000);
	}

	import { onDestroy } from 'svelte';
	onDestroy(() => {
		if (redirectTimer) clearInterval(redirectTimer);
	});
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>{$t('auth.emailVerification')}</title>
	<meta name="description" content="Fortuna Flow - {$t('auth.emailVerification')}" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>{$t('auth.emailVerification')}</h1>
		<p>{$t('auth.enterEmailForVerification')}</p>
		
		{#if status === 'success'}
			<div class="success-message">
				<p>{$t('auth.verificationEmailSent')}</p>
				<p>{$t('auth.checkEmailAndClick')}</p>
				<p style="margin-top: 10px; color: var(--color-text-secondary); font-size: 0.95rem;">
					{$t('auth.redirectingToSigninIn')} {redirectCountdown} {redirectCountdown === 1 ? $t('auth.second') : $t('auth.seconds')}...
				</p>
				<div class="form-button">
					<button type="button" class="glassy-button" on:click={() => goto('/auth/signin')}>
						{$t('auth.signin')}
					</button>
				</div>
			</div>
		{:else}
			<form class="form" on:submit={handleSendVerification} autocomplete="on">
				<div class="form-field">
					<input 
						type="email" 
						name="email" 
						placeholder={$t('auth.enterEmailAddress')} 
						bind:value={email} 
						required 
						disabled={loading}
					/>
				</div>
				<div class="form-button">
					<button type="submit" class="glassy-button" disabled={loading}>
						{loading ? $t('auth.sending') : $t('auth.sendVerification')}
					</button>
				</div>
			</form>
			{#if status === 'error'}
				<div class="error-info">
					<p>{$t('auth.failedToSendVerification')}</p>
					<p>{errorMessage}</p>
				</div>
			{/if}
		{/if}
		
		<div class="auth-links">
			<p>{$t('auth.alreadyHaveAccount')} <a href="/auth/signin">{$t('auth.signinHere')}</a></p>
			<p>{$t('auth.dontHaveAccount')} <a href="/auth/signup">{$t('auth.signupHere')}</a></p>
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