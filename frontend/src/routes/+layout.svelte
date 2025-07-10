<script lang="ts">
	import './styles.css';
	import './dark-mode.css';
	import '$lib/components/components.css';
	import { onMount, onDestroy } from 'svelte';
	import { token, darkMode } from '$lib/store';
	import { goto } from '$app/navigation';
	import { navigating } from '$app/stores';
	import { refreshAccessToken } from '$lib/apis/users';
	import { isTokenExpired } from '$lib/utils';

	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import SplashScreen from '$lib/components/SplashScreen.svelte';
	import PreloadingIndicator from '$lib/components/PreloadingIndicator.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';

	let showSplash = true;
	let isNavigating = false;
	let intervalId: number;

	async function handleTokenOnMount() {
		// console.log('onMount layout running', $token, window.location.pathname);
		const currentToken = $token;

		if (currentToken) {
			// console.log('Token exists:', currentToken);
			if (isTokenExpired(currentToken)) {
				// console.log('Token expired, trying to refresh...');
				await refreshAccessToken();
			} 
			return;
		}

		const isAuthPage = /^\/auth\/(signin|signup|callback)$/.test(window.location.pathname);
		if (!isAuthPage) {
			// console.log('Refresh token found in cookie, trying to refresh...');
			await refreshAccessToken();
			if ($token) {
				// console.log('Token successfully refreshed');
				window.location.reload();
			} else {
				// console.log('No refresh token found, redirecting to /auth/signin');
				window.location.href = '/auth/signin';
			}
		} else {
			// console.log('No token and on auth page');
			return;
		}
	}

	onMount(async () => {
		await handleTokenOnMount();

		// Splash screen logic
		setTimeout(() => {
			showSplash = false;
		}, 2000);

		intervalId = setInterval(async () => {
			const currentToken = $token;
			if (currentToken && isTokenExpired(currentToken)) {
				console.log('Token expired (interval), refreshing...');
				await refreshAccessToken();
			}
		}, 1000);
	});

	onDestroy(() => {
		clearInterval(intervalId);
	});

	// Sometimes, this may not work because the page moves too quickly during navigation.
	$: if ($navigating) {
		isNavigating = true;
		// console.log('Navigating started', isNavigating);
		$navigating.complete.then(() => {
			isNavigating = false;
			// console.log('Navigating ended', isNavigating);
		});
	}
</script>

{#if isNavigating}
	<PreloadingIndicator />
{/if}

{#if showSplash}
	<SplashScreen show={showSplash} />
{:else}
	<div class="app">
		{#if $token}
			<Header />
		{/if}
		<main>
			<slot />
		</main>
		{#if $token}
			<Footer />
			<FloatingButton />
		{/if}
	</div>
{/if}

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 30rem;
		margin: 0 auto;
		margin-top: 70px;
		box-sizing: border-box;
	}

	@media only screen and (max-width: 480px) {
		main {
			margin-top: 60px;
			margin-bottom: 60px;
		}
	}
</style>
