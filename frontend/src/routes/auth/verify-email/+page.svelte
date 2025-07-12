<script lang="ts">
	import '../auth.css';
	import { goto } from '$app/navigation';
	import { Toaster, toast } from 'svelte-sonner';
	import { verifyEmail } from '$lib/apis/auth';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { onDestroy } from 'svelte';

	let token = '';
	let loading = false;
	let status: 'verifying' | 'success' | 'error' = 'verifying';
	let errorMessage = '';
	let redirectCountdown = 10;
	let redirectTimer: ReturnType<typeof setInterval> | null = null;

	// Get token from URL parameter if available
	$: if ($page.url.searchParams.get('token')) {
		token = $page.url.searchParams.get('token') || '';
	}

	onMount(async () => {
		if (token) {
			loading = true;
			try {
				const data = await verifyEmail(token);
				status = 'success';
				toast.success(data.message || 'Email verified successfully!');
				startRedirectCountdown();
			} catch (error: any) {
				status = 'error';
				if (error.detail) {
					errorMessage = error.detail;
				} else if (error.message) {
					errorMessage = error.message;
				} else if (typeof error === 'string') {
					errorMessage = error;
				} else {
					errorMessage = 'Failed to verify email. Please try again.';
				}
				toast.error(errorMessage);
			}
			loading = false;
		}
	});

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

	// Clean up timer on destroy
	onDestroy(() => {
		if (redirectTimer) clearInterval(redirectTimer);
	});
</script>

<Toaster richColors position="top-center" />

<svelte:head>
	<title>Verify Email</title>
	<meta name="description" content="Fortuna Flow - Verify Email" />
</svelte:head>

<div class="auth">
	<div class="form glassy">
		<h1>Verify Email</h1>

		{#if status === 'verifying'}
			<div class="auto-verifying">
				<p class="verifying"><span aria-label="search" role="img">🔍</span> Verifying your email...</p>
				<p>Please wait while we verify your email address.</p>
			</div>
		{:else if status === 'success'}
			<div class="success-message">
				<p>✅ Email verified successfully!</p>
				<p>Your email has been verified. You can now sign in to your account.</p>
				<p style="margin-top: 10px; color: var(--color-text-secondary); font-size: 0.95rem;">
					Redirecting to sign in in {redirectCountdown} second{redirectCountdown === 1 ? '' : 's'}...
				</p>
				<div class="form-button">
					<button type="button" class="glassy-button" on:click={() => goto('/auth/signin')}>
						Sign in
					</button>
				</div>
			</div>
		{:else if status === 'error'}
			<div class="error-info">
				<p>❌ Verification failed.</p>
				<p>{errorMessage}</p>
			</div>
			<div class="form-button">
				<button type="button" class="glassy-button" on:click={() => goto('/auth/send-verification')}>
					Resend verification
				</button>
			</div>
			<div class="auth-links">
				<p>Already have an account? <a href="/auth/signin">Sign in</a></p>
			</div>
		{/if}
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

	.verifying {
		color: var(--color-success);
		font-weight: 600;
		font-size: 1.1rem;
	}
</style> 