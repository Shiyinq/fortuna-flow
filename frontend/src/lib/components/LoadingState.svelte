<script lang="ts">
	export let message: string = 'Please wait while we load your data.';
</script>

<div class="loading-state glassy">
	<h3>Loading...</h3>
	<p>{message}</p>
</div>

<style>
	.loading-state {
		width: 100%;
		padding: 40px 20px;
		text-align: center;
		border-radius: 16px;
		color: #222;
	}

	/* Dark mode loading state */
	:global(:root.dark) .loading-state {
		color: #f1f5f9;
	}

	.loading-state h3 {
		margin: 0 0 16px 0;
		font-size: 1.5rem;
		font-weight: 600;
	}

	.loading-state p {
		margin: 0;
		font-size: 1rem;
		opacity: 0.8;
	}
</style> 