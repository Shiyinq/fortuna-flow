<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { sendVerificationEmail } from '$lib/apis/auth';

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
			toast.error('Please enter a valid email address');
			return;
		}
		
		loading = true;
		try {
			const data = await sendVerificationEmail(email);
			toast.success(data.message || 'Verification email sent successfully!');
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
				errorMessage = 'Failed to send verification email. Please try again.';
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
	<title>Send Verification Email</title>
	<meta name="description" content="Fortuna Flow - Send Verification Email" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>Email Verification</h1>
		<p>Enter your email address to receive a verification link</p>
		
		{#if status === 'success'}
			<div class="success-message">
				<p>✅ Verification email sent successfully!</p>
				<p>Please check your email and click the verification link.</p>
				<p style="margin-top: 10px; color: var(--color-text-secondary); font-size: 0.95rem;">
					Redirecting to sign in in {redirectCountdown} second{redirectCountdown === 1 ? '' : 's'}...
				</p>
				<div class="form-button">
					<button type="button" class="glassy-button" on:click={() => goto('/auth/signin')}>
						Sign in
					</button>
				</div>
			</div>
		{:else}
			<form class="form" on:submit={handleSendVerification} autocomplete="on">
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
						{loading ? 'Sending...' : 'Send Verification'}
					</button>
				</div>
			</form>
			{#if status === 'error'}
				<div class="error-info">
					<p>❌ Failed to send verification email.</p>
					<p>{errorMessage}</p>
				</div>
			{/if}
		{/if}
		
		<div class="auth-links">
			<p>Already have an account? <a href="/auth/signin">Sign in</a></p>
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