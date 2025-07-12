<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { resetPassword } from '$lib/apis/auth';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();

	let token = '';
	let newPassword = '';
	let confirmPassword = '';
	let loading = false;
	let showPassword = false;
	let showConfirmPassword = false;
	let hasTokenFromUrl = false;

	const upperCaseRegex = /[A-Z]/;
	const lowerCaseRegex = /[a-z]/;
	const numberRegex = /\d/;
	const symbolRegex = /[!@#$%^&*(),.?":{}|<>]/;
	const noSpaceRegex = /^\S*$/;

	// Get token from URL parameter if available
	$: if ($page.url.searchParams.get('token')) {
		token = $page.url.searchParams.get('token') || '';
		hasTokenFromUrl = true;
	}

	const validatePassword = (password: string) => {
		const minLength = 8;
		const hasUpperCase = upperCaseRegex.test(password);
		const hasLowerCase = lowerCaseRegex.test(password);
		const hasNumbers = numberRegex.test(password);
		const hasSymbols = symbolRegex.test(password);
		const noSpaces = noSpaceRegex.test(password);

		return {
			isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSymbols && noSpaces,
			errors: {
				length: password.length < minLength ? `Minimum ${minLength} characters` : null,
				uppercase: !hasUpperCase ? 'Must have uppercase letter' : null,
				lowercase: !hasLowerCase ? 'Must have lowercase letter' : null,
				numbers: !hasNumbers ? 'Must have number' : null,
				symbols: !hasSymbols ? 'Must have symbol' : null,
				spaces: !noSpaces ? 'No spaces allowed' : null
			}
		};
	};

	const handleResetPassword = async (event: Event) => {
		event.preventDefault();
		
		// Basic token validation
		if (!token || token.trim().length === 0) {
			toast.error($t('auth.enterResetToken'));
			return;
		}
		
		// Validate password
		const passwordValidation = validatePassword(newPassword);
		if (!passwordValidation.isValid) {
			toast.error($t('auth.passwordCriteriaNotMet'));
			return;
		}

		// Validate password confirmation
		if (newPassword !== confirmPassword) {
			toast.error($t('auth.passwordMismatch'));
			return;
		}

		loading = true;
		try {
			const data = await resetPassword(token, newPassword, confirmPassword);
			toast.success(data.message || $t('auth.passwordResetSuccess'));
			// Clear the form
			token = '';
			newPassword = '';
			confirmPassword = '';
			// Redirect after a short delay to show the success message
			setTimeout(() => {
				goto('/auth/signin');
			}, 2000);
		} catch (error: any) {
			console.error('Reset password error:', error);
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

	// Check for token on mount
	onMount(() => {
		const urlToken = $page.url.searchParams.get('token');
		if (urlToken) {
			token = urlToken;
			hasTokenFromUrl = true;
		}
	});
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>{$t('auth.resetPassword')}</title>
	<meta name="description" content="Fortuna Flow - {$t('auth.resetPassword')}" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>{$t('auth.resetPassword')}</h1>
		<p>
			{hasTokenFromUrl 
				? $t('auth.enterNewPassword') 
				: $t('auth.enterTokenAndPassword')
			}
		</p>
		<form class="form" on:submit={handleResetPassword} autocomplete="on">
			{#if !hasTokenFromUrl}
				<div class="form-field">
					<input 
						type="text" 
						name="token" 
						placeholder={$t('auth.enterResetToken')} 
						bind:value={token} 
						required 
						disabled={loading}
					/>
				</div>
			{/if}
			<div class="form-field password-input">
				<input 
					type="password"
					name="newPassword" 
					placeholder={$t('auth.newPassword')} 
					bind:value={newPassword} 
					required 
					disabled={loading}
				/>
			</div>
			<div class="form-field password-input">
				<input 
					type="password"
					name="confirmPassword" 
					placeholder={$t('auth.confirmNewPassword')} 
					bind:value={confirmPassword} 
					required 
					disabled={loading}
				/>
			</div>

			{#if newPassword}
				<div class="password-requirements">
					<ul>
						<li class={confirmPassword === newPassword ? 'valid' : 'invalid'}>{$t('auth.passwordMatch')}</li>
						<li class={newPassword.length >= 8 ? 'valid' : 'invalid'}>{$t('auth.minimum8Characters')}</li>
						<li class={upperCaseRegex.test(newPassword) ? 'valid' : 'invalid'}>{$t('auth.atLeast1Uppercase')}</li>
						<li class={lowerCaseRegex.test(newPassword) ? 'valid' : 'invalid'}>{$t('auth.atLeast1Lowercase')}</li>
						<li class={numberRegex.test(newPassword) ? 'valid' : 'invalid'}>{$t('auth.atLeast1Number')}</li>
						<li class={symbolRegex.test(newPassword) ? 'valid' : 'invalid'}>{$t('auth.atLeast1Symbol')}</li>
						<li class={noSpaceRegex.test(newPassword) ? 'valid' : 'invalid'}>{$t('auth.noSpacesAllowed')}</li>
					</ul>
				</div>
			{/if}

			<div class="form-button">
				<button type="submit" class="glassy-button" disabled={loading}>
					{loading ? $t('common.loading') : $t('auth.resetPassword')}
				</button>
			</div>
		</form>
		<div class="auth-links">
			<p>{$t('auth.noResetEmail')} <a href="/auth/forgot-password">{$t('auth.resend')}</a></p>
			<p>{$t('auth.rememberPassword')} <a href="/auth/signin">{$t('auth.signin')}</a></p>
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

	.form-field {
		position: relative;
	}

	.form-field input {
		width: 100%;
		padding: 12px;
		border: 1px solid var(--color-border);
		border-radius: 10px;
	}

	.password-input {
		position: relative;
	}

	.password-input input {
		padding-right: 40px;
	}

	.password-requirements {
		margin-top: 16px;
		margin-bottom: 24px;
		background: #f3f6fb;
		border-radius: 16px;
		padding: 18px 24px;
		border: none;
		box-shadow: none;
	}

	.password-requirements ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.password-requirements li {
		display: flex;
		align-items: center;
		font-size: 0.98rem;
		margin-bottom: 8px;
		padding-left: 0;
		font-weight: 500;
	}

	.password-requirements li:last-child {
		margin-bottom: 0;
	}

	.password-requirements li.valid {
		color: #22bb55;
	}

	.password-requirements li.invalid {
		color: #e53935;
	}
</style> 