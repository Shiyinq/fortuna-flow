<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { forgotPassword } from '$lib/apis/auth';
	import { onDestroy } from 'svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();

	let email = '';
	let loading = false;
	let submitted = false;
	let redirectCountdown = 10;
	let redirectTimer: ReturnType<typeof setInterval> | null = null;

	const handleForgotPassword = async (event: Event) => {
		event.preventDefault();
		
		// Basic email validation
		if (!email || !email.includes('@')) {
			toast.error($t('auth.invalidEmail'));
			return;
		}
		
		loading = true;
		try {
			const data = await forgotPassword(email);
			toast.success(data.message || $t('auth.passwordResetSent'));
			submitted = true;
			// Clear the form
			email = '';
			// Redirect after a short delay to show the success message
			startRedirectCountdown();
		} catch (error: any) {
			console.error('Forgot password error:', error);
			if (error.detail) {
				toast.error(error.detail);
			} else if (error.message) {
				toast.error(error.message);
			} else if (typeof error === 'string') {
				toast.error(error);
			} else {
				toast.error($t('auth.passwordResetFailed'));
			}
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

	onDestroy(() => {
		if (redirectTimer) clearInterval(redirectTimer);
	});
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>{$t('auth.forgotPassword')}</title>
	<meta name="description" content="Fortuna Flow - {$t('auth.forgotPassword')}" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>{$t('auth.forgotPassword')}</h1>
		<p>{$t('auth.forgotPasswordDescription')}</p>
		
		{#if submitted}
			<div class="success-message">
				<p>✅ {$t('auth.passwordResetSent')}</p>
				<p>{$t('auth.checkEmailForReset')}</p>
				<p style="margin-top: 10px; color: var(--color-text-secondary); font-size: 0.95rem;">
					{$t('auth.redirectingToSignin')} {redirectCountdown} {$t('auth.seconds')}...
				</p>
			</div>
		{:else}
			<form class="form" on:submit={handleForgotPassword} autocomplete="on">
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
						{loading ? $t('common.loading') : $t('auth.sendResetPassword')}
					</button>
				</div>
			</form>
		{/if}
		
		<div class="auth-links">
			<p>{$t('auth.rememberPassword')} <a href="/auth/signin">{$t('auth.signin')}</a></p>
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