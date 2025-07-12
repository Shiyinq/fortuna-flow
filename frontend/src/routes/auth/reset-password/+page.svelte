<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { resetPassword } from '$lib/apis/auth';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

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
			toast.error('Please enter a reset password token');
			return;
		}
		
		// Validate password
		const passwordValidation = validatePassword(newPassword);
		if (!passwordValidation.isValid) {
			toast.error('Password does not meet security criteria');
			return;
		}

		// Validate password confirmation
		if (newPassword !== confirmPassword) {
			toast.error('Password and confirmation password do not match');
			return;
		}

		loading = true;
		try {
			const data = await resetPassword(token, newPassword, confirmPassword);
			toast.success(data.message || 'Password reset successfully!');
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
				toast.error('Failed to reset password. Please try again.');
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
	<title>Reset Password</title>
	<meta name="description" content="Fortuna Flow - Reset Password" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>Reset Password</h1>
		<p>
			{hasTokenFromUrl 
				? 'Please enter your new password below.' 
				: 'Enter the reset password token and your new password'
			}
		</p>
		<form class="form" on:submit={handleResetPassword} autocomplete="on">
			{#if !hasTokenFromUrl}
				<div class="form-field">
					<input 
						type="text" 
						name="token" 
						placeholder="Enter reset password token" 
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
					placeholder="New password" 
					bind:value={newPassword} 
					required 
					disabled={loading}
				/>
			</div>
			<div class="form-field password-input">
				<input 
					type="password"
					name="confirmPassword" 
					placeholder="Confirm new password" 
					bind:value={confirmPassword} 
					required 
					disabled={loading}
				/>
			</div>

			{#if newPassword}
				<div class="password-requirements">
					<ul>
						<li class={confirmPassword === newPassword ? 'valid' : 'invalid'}>Password match</li>
						<li class={newPassword.length >= 8 ? 'valid' : 'invalid'}>Minimum 8 characters</li>
						<li class={upperCaseRegex.test(newPassword) ? 'valid' : 'invalid'}>At least 1 uppercase letter</li>
						<li class={lowerCaseRegex.test(newPassword) ? 'valid' : 'invalid'}>At least 1 lowercase letter</li>
						<li class={numberRegex.test(newPassword) ? 'valid' : 'invalid'}>At least 1 number</li>
						<li class={symbolRegex.test(newPassword) ? 'valid' : 'invalid'}>At least 1 symbol</li>
						<li class={noSpaceRegex.test(newPassword) ? 'valid' : 'invalid'}>No spaces allowed</li>
					</ul>
				</div>
			{/if}

			<div class="form-button">
				<button type="submit" class="glassy-button" disabled={loading}>
					{loading ? 'Resetting...' : 'Reset Password'}
				</button>
			</div>
		</form>
		<div class="auth-links">
			<p>No reset email? <a href="/auth/forgot-password">Resend</a></p>
			<p>Remember your password? <a href="/auth/signin">Sign in</a></p>
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