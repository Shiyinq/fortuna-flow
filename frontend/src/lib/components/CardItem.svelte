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

<div 
	class="card-item {className}" 
	class:clickable={onClick !== null}
	on:click={onClick || undefined}
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
</div>

<style>
	.card-item {
		width: 100%;
		padding: 16px;
		display: flex;
		border-radius: 12px;
		margin-bottom: 8px;
		background: rgba(44,62,80,0.08);
		border: 1px solid rgba(44,62,80,0.10);
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
	}

	/* Hover effect removed to keep items static like "Recent total spends" */

	.card-item.clickable {
		cursor: pointer;
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
	}

	.card-item-title {
		font-size: 14px;
		font-weight: 600;
		color: #222;
		margin: 0;
	}

	.card-item-subtitle {
		font-size: 12px;
		color: #555;
		margin: 0;
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