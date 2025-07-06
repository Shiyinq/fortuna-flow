<script lang="ts">
	export let message: string = 'Please wait while we load your data.';
</script>

<div class="loading-state">
	<h3>Loading...</h3>
	<p>{message}</p>
</div>

<style>
	.loading-state {
		width: 100%;
		padding: 40px 20px;
		text-align: center;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15), 0 1.5px 4px rgba(44,62,80,0.08);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.loading-state:hover {
		background: rgba(255,255,255,0.7);
		box-shadow: 0 12px 40px rgba(180, 200, 220, 0.2), 0 2px 8px rgba(44,62,80,0.12);
		transform: translateY(-1px);
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