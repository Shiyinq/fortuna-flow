<script>
	import { onMount } from 'svelte';
	let p = 0;
	let visible = false;
	onMount(() => {
		visible = true;
		function next() {
			p += 0.1;
			const remaining = 1 - p;
			if (remaining > 0.15) setTimeout(next, 500 / remaining);
		}
		setTimeout(next, 250);
	});
</script>

{#if visible}
	<div class="progress-container">
		<div class="progress" style="width: {p * 100}%" />
	</div>
{/if}

<style>
	.progress-container {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 4px;
		z-index: 9999999;
	}

	.progress {
		position: absolute;
		left: 0;
		top: 0;
		height: 100%;
		background: linear-gradient(90deg, var(--color-theme-1), var(--color-theme-2));
		transition: width 0.4s;
		box-shadow: 0 0 10px rgba(0, 200, 83, 0.3);
	}

	/* Dark mode progress bar */
	:global(:root.dark) .progress {
		background: linear-gradient(90deg, var(--color-theme-1), var(--color-theme-2));
		box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
	}
</style>
