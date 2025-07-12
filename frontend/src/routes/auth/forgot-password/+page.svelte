<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { forgotPassword } from '$lib/apis/auth';
	import { onDestroy } from 'svelte';

	let email = '';
	let loading = false;
	let submitted = false;
	let redirectCountdown = 10;
	let redirectTimer: ReturnType<typeof setInterval> | null = null;

	const handleForgotPassword = async (event: Event) => {
		event.preventDefault();
		
		// Basic email validation
		if (!email || !email.includes('@')) {
			toast.error('Please enter a valid email address');
			return;
		}
		
		loading = true;
		try {
			const data = await forgotPassword(email);
			toast.success(data.message || 'Password reset email sent successfully!');
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
				toast.error('Failed to send password reset email. Please try again.');
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
	<title>Forgot Password</title>
	<meta name="description" content="Fortuna Flow - Forgot Password" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>Forgot Password</h1>
		<p>Enter your email address to receive a password reset link</p>
		
		{#if submitted}
			<div class="success-message">
				<p>✅ Password reset email sent successfully!</p>
				<p>Please check your email and click the reset password link.</p>
				<p style="margin-top: 10px; color: var(--color-text-secondary); font-size: 0.95rem;">
					Redirecting to sign in in {redirectCountdown} second{redirectCountdown === 1 ? '' : 's'}...
				</p>
			</div>
		{:else}
			<form class="form" on:submit={handleForgotPassword} autocomplete="on">
				<div class="form-field">
					<input 
						type="email" 
						name="email" 
						placeholder="Enter your email address" 
						bind:value={email} 
						required 
						disabled={loading}
					/>
				</div>
				<div class="form-button">
					<button type="submit" class="glassy-button" disabled={loading}>
						{loading ? 'Sending...' : 'Send Reset Password'}
					</button>
				</div>
			</form>
		{/if}
		
		<div class="auth-links">
			<p>Remember your password? <a href="/auth/signin">Sign in</a></p>
			<p>Don't have an account? <a href="/auth/signup">Sign up</a></p>
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