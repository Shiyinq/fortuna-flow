<script lang="ts">
	import { onMount } from 'svelte';
	import { token } from '$lib/store';
	import { getCategories } from '$lib/apis/categories';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';

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

<div class="categories glassy">
	<div class="category-header">
		<h5 class="text-heading">My Categories</h5>
		<a href="/transactions/categories/create" class="category-create-link">Create New Category</a>
	</div>
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
</div>

<style>
	h5 {
		margin-top: 0;
	}

	.categories {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		position: relative;
		overflow: hidden;
	}

	.category-header {
		width: 100%;
		display: flex;
		margin-bottom: 16px;
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
	}

	.category-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

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
	}

	.category-info:hover {
		transform: translateY(-2px);
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
	}

	.category-title span {
		font-size: 13px;
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

	.category-create-link {
		font-size: 0.9rem;
		font-weight: 500;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		color: var(--color-theme-1);
		text-decoration: none;
		opacity: 0.9;
		transition: opacity 0.15s;
	}

	.category-create-link:hover {
		opacity: 0.7;
	}
</style>
