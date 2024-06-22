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
	}
</style>
