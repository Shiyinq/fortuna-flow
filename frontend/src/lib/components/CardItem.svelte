<script lang="ts">
	export let icon: string = '';
	export let iconComponent: any = null;
	export let iconProps: any = {};
	export let title: string = '';
	export let subtitle: string = '';
	export let amount: string = '';
	export let type: 'expense' | 'income' | 'neutral' | string = 'neutral';
	export let onClick: (() => void) | null = null;
	export let className: string = '';
</script>

<button 
	class="card-item {className}" 
	class:clickable={onClick !== null}
	on:click={onClick || undefined}
	type="button"
	disabled={!onClick}
>
	<div class="card-item-left">
		{#if icon || iconComponent}
			<div class="card-item-icon">
				{#if iconComponent}
					<svelte:component this={iconComponent} {...iconProps} />
				{:else if icon}
					{@html icon}
				{/if}
			</div>
		{/if}
		<div class="card-item-content">
			{#if title}
				<div class="card-item-title">{title}</div>
			{/if}
			{#if subtitle}
				<div class="card-item-subtitle">{subtitle}</div>
			{/if}
		</div>
	</div>
	
	{#if amount}
		<div class="card-item-amount" class:expense={type === 'expense'} class:income={type === 'income'}>
			{amount}
		</div>
	{/if}
</button>

<style>
	.card-item {
		width: 100%;
		padding: 16px;
		display: flex;
		border-radius: 12px;
		margin-bottom: 8px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
		transition: all 0.3s ease;
		box-shadow: 0 4px 16px rgba(180, 200, 220, 0.08);
	}

	.card-item:hover {
		background: rgba(255,255,255,0.8);
		transform: translateY(-2px);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
	}

	.card-item.clickable {
		cursor: pointer;
	}

	.card-item:disabled {
		cursor: default;
		opacity: 1;
	}

	.card-item-left {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.card-item-icon {
		font-size: 1em;
		margin-right: 8px;
		display: flex;
		align-items: center;
	}

	.card-item-content {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.card-item-title {
		font-size: 14px;
		font-weight: 600;
		color: #222;
		margin: 0;
		text-align: left;
	}

	.card-item-subtitle {
		font-size: 12px;
		color: #555;
		margin: 0;
		text-align: left;
	}

	.card-item-amount {
		font-size: 14px;
		font-weight: 600;
		color: #222;
	}

	.card-item-amount.expense {
		color: #ff6b6b;
	}

	.card-item-amount.income {
		color: #51cf66;
	}

	.card-item:last-child {
		margin-bottom: 0;
	}
</style> 