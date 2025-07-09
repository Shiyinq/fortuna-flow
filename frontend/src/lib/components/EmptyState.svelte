<script>
	export let emoji = '🚫';
	export let message = 'There is no data available.';
</script>

<div class="empty-state">
	<h1>{emoji}</h1>
	<p>{message}</p>
</div>

<style>
	.empty-state {
		padding: 30px;
		text-align: center;
		color: var(--color-text);
	}

	.empty-state h1 {
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	.empty-state p {
		font-size: 1.1rem;
		opacity: 0.8;
	}
</style>
