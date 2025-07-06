<script lang="ts">
	import { onMount } from 'svelte';
	import { token } from '$lib/store';
	import { getCategories } from '$lib/apis/categories';
	import { goto } from '$app/navigation';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';

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
		<LoadingState message="Loading categories..." />
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
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
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

	.category-header h6 {
		font-size: 0.9rem;
		font-weight: 500;
		margin: 0;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.5px;
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
		background: rgba(44,62,80,0.08);
		border: 1px solid rgba(44,62,80,0.10);
		justify-content: space-between;
		position: relative;
		z-index: 1;
		transition: all 0.3s ease;
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