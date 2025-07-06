<script>
	import './styles.css';
	import { onMount } from 'svelte';
	import { token, darkMode } from '$lib/store';
	import { goto } from '$app/navigation';
	import { navigating } from '$app/stores';

	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import SplashScreen from '$lib/components/SplashScreen.svelte';
	import PreloadingIndicator from '$lib/components/PreloadingIndicator.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';

	let showSplash = true;
	let isNavigating = false;

	onMount(() => {
		// Initialize dark mode from localStorage
		if (typeof window !== 'undefined') {
			const savedDarkMode = localStorage.getItem('darkMode');
			if (savedDarkMode !== null) {
				darkMode.set(savedDarkMode === 'true');
			}
		}
		
		// if (!$token) {
		// 	goto('/auth/signin');
		// }
		setTimeout(() => {
			showSplash = false;
		}, 2000);
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
			margin-top: 45px;
			margin-bottom: 60px;
		}
	}
</style>
