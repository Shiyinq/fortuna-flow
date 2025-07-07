<script lang="ts">
	import { onMount } from 'svelte';
	import { token } from '$lib/store';
	import { getCategories } from '$lib/apis/categories';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let categories: any[] | undefined = undefined;
	export let error: string | undefined = undefined;

	let internalCategories: any[] = [];
	let internalLoading = true;
	let internalError = '';

	const loadCategories = async () => {
		try {
			internalLoading = true;
			const response = await getCategories($token, 1, 100);
			internalCategories = response.data || [];
		} catch (err: any) {
			internalError = err.detail || 'Failed to load categories';
		} finally {
			internalLoading = false;
		}
	};

	onMount(() => {
		if (categories === undefined) {
			loadCategories();
		} else {
			internalLoading = false;
		}
	});
</script>

<Card
	title="My Categories"
	subtitle="New Category"
	subtitleLink="/transactions/categories/create"
	marginBottom={'0px'}
	marginTop={'0px'}
	showGradient={true}
	highlightTitle={true}
>
	{#if internalLoading}
		<LoadingState message="Loading categories..." />
	{:else if error ?? internalError}
		<div class="error">{error ?? internalError}</div>
	{:else if !(categories ?? internalCategories).length}
		<EmptyState />
	{:else}
		{#each categories ?? internalCategories as category}
			<div class="category-info glassy-light">
				<div class="category-title">
					<span class="category-icon">{category.categoryIcon || '📁'}</span>
					<span>{category.name}</span>
				</div>
				<div class="category-type">
					<span class="type-badge {category.type}">
						{category.type === 'expense' ? 'Expense' : 'Income'}
					</span>
				</div>
			</div>
		{/each}
	{/if}
</Card>

<style>
	.error {
		text-align: center;
		padding: 20px;
		color: var(--color-error);
	}

	.category-info {
		width: 100%;
		padding: 16px;
		display: flex;
		border-radius: 12px;
		margin-bottom: 12px;
		justify-content: space-between;
		position: relative;
		z-index: 1;
		transition: all 0.3s ease;
		color: var(--color-text-heading);
		background: var(--glassy-bg-light);
		border: 1px solid var(--glassy-border);
		box-shadow: 0 4px 16px var(--glassy-shadow-light), 0 1px 4px rgba(44, 62, 80, 0.08);
	}

	.category-info:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 24px rgba(var(--color-theme-1-rgb), 0.18), 0 2px 8px rgba(44, 62, 80, 0.12);
	}

	.category-title {
		gap: 0.4rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.category-icon {
		font-size: 1em;
		margin-right: 8px;
		color: var(--color-text-heading);
	}

	.category-title span {
		font-size: 13px;
		color: var(--color-text-heading);
	}

	.category-type {
		display: flex;
		align-items: center;
	}

	.type-badge {
		font-size: 11px;
		padding: 2px 6px;
		border-radius: 4px;
		font-weight: 500;
		text-transform: uppercase;
	}

	.type-badge.expense {
		background: rgba(239, 68, 68, 0.1);
		color: #ef4444;
	}

	.type-badge.income {
		background: rgba(34, 197, 94, 0.1);
		color: #22c55e;
	}
</style>
