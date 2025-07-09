<script lang="ts">
	import { page } from '$app/stores';
	import { numberToEmoji } from '$lib/utils';
	import Button from '$lib/components/Button.svelte';

	let status = $page.status;
	let description = $page.error?.message || 'Error';
</script>

<svelte:head>
	<title>{status} - {description}</title>
	<meta name="description" content="Fortuna Flow - {description}" />
</svelte:head>

<div class="error-container">
	<h1>{numberToEmoji(status)}</h1>
	<p>Page {description}. Let's get you back on track!</p>
	<Button variant="primary-solid" size="medium" on:click={() => window.location.href = '/'}>
		🚀 Back to Home
	</Button>
</div>

<style>
	.error-container {
		height: 80vh;
		display: flex;
		text-align: center;
		align-items: center;
		flex-direction: column;
		justify-content: center;
	}

	h1 {
		padding: 0;
		margin: 0;
		font-size: 70px;
	}

	p {
		margin: 16px 0 24px 0;
		font-size: 1.2rem;
		color: var(--color-theme-1);
		font-weight: 500;
		letter-spacing: 0.5px;
	}
</style>
