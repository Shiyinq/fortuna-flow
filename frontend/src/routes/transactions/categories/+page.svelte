<script lang="ts">
	import { onMount } from 'svelte';
	import { token } from '$lib/store';
	import { getCategories } from '$lib/apis/categories';
	import { goto } from '$app/navigation';
	import EmptyState from '$lib/components/EmptyState.svelte';

	export let data: any;

	let categories: any[] = [];
	let loading = true;
	let error = '';

	const loadCategories = async () => {
		try {
			loading = true;
			const response = await getCategories($token, 1, 100);
			categories = response.data || [];
		} catch (err: any) {
			error = err.detail || 'Failed to load categories';
		} finally {
			loading = false;
		}
	};

	onMount(() => {
		loadCategories();
	});
</script>

<svelte:head>
	<title>Categories</title>
	<meta name="description" content="Fortuna Flow - Manage Categories" />
</svelte:head>

<div class="categories">
	<div class="category-header">
		<h5>My Categories</h5>
		<a href="/transactions/categories/create"><h6>Create New Category</h6></a>
	</div>
	{#if loading}
		<div class="loading">Loading categories...</div>
	{:else if error}
		<div class="error">{error}</div>
	{:else if !categories.length}
		<EmptyState />
	{:else}
		{#each categories as category}
			<div class="category-info">
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
	h5,
	h6 {
		margin-top: 0;
	}

	.categories {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	.category-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}

	.loading, .error {
		text-align: center;
		padding: 20px;
	}

	.error {
		color: var(--color-error);
	}

	.category-info {
		width: 100%;
		padding: 12px;
		display: flex;
		border-radius: 8px;
		margin-bottom: 8px;
		background-color: #fff;
		justify-content: space-between;
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
</style> 