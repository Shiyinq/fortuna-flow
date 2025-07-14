<script lang="ts">
	import '../auth.css';
	import { Toaster, toast } from 'svelte-sonner';
	import { FORTUNA_API_BASE_URL } from '$lib/constants';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import { userSignUp } from '$lib/apis/auth';

	const { t } = useTranslation();

	let name = '';
	let username = '';
	let email = '';
	let password = '';
	let confirmPassword = '';
	let loading = false;

	const handleSignUp = async (event: Event) => {
		event.preventDefault();
		loading = true;
		
		// Client-side validation
		if (!name || !username || !email || !password || !confirmPassword) {
			toast.error($t('auth.formNotValid'));
			loading = false;
			return;
		}

		if (password !== confirmPassword) {
			toast.error($t('auth.passwordMismatch'));
			loading = false;
			return;
		}

		try {
			const data = await userSignUp(name, username, email, password, confirmPassword);
			toast.success(data.detail || $t('auth.signupSuccess'));
			// Clear form
			name = '';
			username = '';
			email = '';
			password = '';
			confirmPassword = '';
		} catch (e: any) {
			let errorMessage = $t('auth.signupFailed');
			if (e?.detail) {
				switch (e.detail) {
					case 'Username already exist.':
						errorMessage = $t('auth.usernameTaken');
						break;
					case 'Email already exist.':
						errorMessage = $t('auth.emailTaken');
						break;
					case 'The two passwords did not match.':
						errorMessage = $t('auth.passwordMismatch');
						break;
					case 'Password must contain at least 8 characters, including uppercase, lowercase, digits, and symbols. No spaces allowed.':
						errorMessage = $t('auth.passwordRules');
						break;
					case 'Too many requests. Please try again later.':
					case 'Too manyrRequests':
						errorMessage = $t('auth.tooManyRequests');
						break;
					default:
						errorMessage = e.detail;
				}
			} else if (e?.message) {
				errorMessage = e.message;
			}
			console.error('Sign up error:', e);
			toast.error(errorMessage);
		} finally {
			loading = false;
		}
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
		<form class="form" on:submit={handleSignUp} autocomplete="on">
			<div class="form-field">
				<input type="text" name="name" placeholder={$t('profile.fullName')} bind:value={name} required />
			</div>
			<div class="form-field">
				<input type="text" name="username" placeholder={$t('auth.username')} bind:value={username} required />
			</div>
			<div class="form-field">
				<input type="email" name="email" placeholder={$t('auth.email')} bind:value={email} required />
			</div>
			<div class="form-field">
				<input type="password" name="password" placeholder={$t('auth.password')} bind:value={password} required />
			</div>
			<div class="form-field">
				<input type="password" name="confirmPassword" placeholder={$t('auth.confirmPassword')} bind:value={confirmPassword} required />
			</div>
			<div class="form-button">
				<button type="submit" class="glassy-button" disabled={loading}>{loading ? $t('common.loading') : $t('auth.signup')}</button>
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
