<script lang="ts">
	export let title: string = '';
	export let subtitle: string = '';
	export let subtitleLink: string = '';
	export let showGradient: boolean = false;
	export let padding: string = '20px';
	export let marginBottom: string = '16px';
    export let marginTop: string = '16px';
	export let className: string = '';
</script>

<div class="cards {className}" style="padding: {padding}; margin-bottom: {marginBottom}; margin-top: {marginTop}">
	{#if showGradient}
		<div class="card-gradient"></div>
	{/if}
	
	{#if title || subtitle}
		<div class="card-header">
			{#if title}
				<h5>{title}</h5>
			{/if}
			{#if subtitle}
				{#if subtitleLink}
					<a href={subtitleLink}><h6>{subtitle}</h6></a>
				{:else}
					<h6>{subtitle}</h6>
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
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15), 0 1.5px 4px rgba(44,62,80,0.08);
		position: relative;
		overflow: visible;
		z-index: 1;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.cards:hover {
		background: rgba(255,255,255,0.7);
		box-shadow: 0 12px 40px rgba(180, 200, 220, 0.2), 0 2px 8px rgba(44,62,80,0.12);
		transform: translateY(-1px);
	}

	.card-gradient {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
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
	}
</style> 