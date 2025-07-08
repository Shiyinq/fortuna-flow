<script lang="ts">
	export let title: string = '';
	export let subtitle: string = '';
	export let subtitleLink: string = '';
	export let showGradient: boolean = false;
	export let padding: string = '20px';
	export let marginBottom: string = '16px';
	export let marginTop: string = '16px';
	export let className: string = '';
	export let highlightTitle: boolean = false;
	export let highlightTotal: boolean = false;
</script>

<div
	class="cards glassy {className}"
	style="padding: {padding}; margin-bottom: {marginBottom}; margin-top: {marginTop}"
>
	{#if showGradient}
		<div class="card-gradient"></div>
	{/if}

	{#if title || subtitle}
		<div class="card-header">
			{#if title}
				<h5 class:text-heading={!highlightTitle} class:highlight-title={highlightTitle}>
					{@html title}
				</h5>
			{/if}
			{#if subtitle}
				{#if subtitleLink}
					<a href={subtitleLink}><h6 class:highlight-total={highlightTotal}>{subtitle}</h6></a>
				{:else}
					<h6 class:text-secondary={!highlightTotal} class:highlight-total={highlightTotal}>{subtitle}</h6>
				{/if}
			{/if}
		</div>
	{/if}

	<div class="card-content">
		<slot />
	</div>
</div>

<style>
	.cards {
		width: 100%;
		border-radius: 16px;
		color: #222;
		position: relative;
		overflow: visible;
		z-index: 1;
	}

	.card-gradient {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			45deg,
			rgba(255, 255, 255, 0.1) 0%,
			transparent 50%,
			rgba(255, 255, 255, 0.1) 100%
		);
		pointer-events: none;
		border-radius: 16px;
	}

	.card-header {
		width: 100%;
		display: flex;
		margin-bottom: 16px;
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
	}

	.card-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.card-header h6 {
		font-size: 0.9rem;
		font-weight: 500;
		margin: 0;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.card-header a {
		text-decoration: none;
		color: var(--color-theme-1);
	}

	.card-header a:hover {
		opacity: 0.8;
	}

	.card-content {
		position: relative;
		z-index: 1;
		padding: 16px;
	}

	.highlight-title {
		color: var(--color-theme-1, #00e6b8);
		font-weight: 600;
	}
	.highlight-total {
		color: #888;
		font-size: 0.95rem;
		font-weight: 500;
	}
</style>
