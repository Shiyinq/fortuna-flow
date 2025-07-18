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
	import { Toaster } from 'svelte-sonner';
	import { initI18n, loadSavedLanguage } from '$lib/i18n';

	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import SplashScreen from '$lib/components/SplashScreen.svelte';
	import PreloadingIndicator from '$lib/components/PreloadingIndicator.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';

	let showSplash = true;
	let isNavigating = false;
	let intervalId: number;

	async function tryRefreshAndRedirect() {
		await refreshAccessToken();
		if ($token) {
			window.location.reload();
		} else {
			window.location.href = '/auth/signin';
		}
	}

	async function handleTokenOnMount() {
		const currentToken = $token;

		if (currentToken) {
			if (isTokenExpired(currentToken)) {
				await tryRefreshAndRedirect();
			}
			return;
		}

		const isAuthPage = /^\/auth\/(signin|signup|callback|send-verification|verify-email|forgot-password|reset-password)$/.test(window.location.pathname);
		if (!isAuthPage) {
			await tryRefreshAndRedirect();
		} else {
			return;
		}
	}

	onMount(async () => {
		// Initialize i18n
		loadSavedLanguage();
		initI18n();

		await handleTokenOnMount();

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
		$navigating.complete.then(() => {
			isNavigating = false;
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
		<Toaster richColors position="top-center" />
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
