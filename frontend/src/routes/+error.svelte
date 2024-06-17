<script lang="ts">
	import { page } from '$app/stores';
	import { numberToEmoji } from '$lib/utils';

	let errorMessage = $page.error?.message || 'Error';
	let info = 'Let\'s get you back on track!';
</script>

<svelte:head>
	<title>{errorMessage}</title>
	<meta name="description" content={errorMessage + '. ' + info} />
</svelte:head>

<div class="error-container">
	<h1>{numberToEmoji($page.status)}</h1>
	<p>Page {errorMessage}. {info}</p>
	<a href="/" class="nb-button default">🚀 Back to Home</a>
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

    .error-container a {
		color: var(--color-text);
        border-radius: 8px !important;
        border: 2px solid var(--color-theme-1);
    }
	h1 {
		padding: 0;
		margin: 0;
		font-size: 70px;
	}
</style>
