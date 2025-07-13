<script lang="ts">
	import { t } from '$lib/i18n';
	
	type EmptyStateType = 'noData' | 'noTransactions' | 'noBudgets' | 'noCategories' | 'noWallets' | 'noResults';
	
	export let type: EmptyStateType = 'noData';
	export let customMessage = '';
	export let customEmoji = '';
	
	const emojiMap: Record<EmptyStateType, string> = {
		noData: '📊',
		noTransactions: '💰',
		noBudgets: '📋',
		noCategories: '🏷️',
		noWallets: '💳',
		noResults: '🔍'
	};
	
	const messageMap: Record<EmptyStateType, string> = {
		noData: 'common.emptyState.noData',
		noTransactions: 'common.emptyState.noTransactions',
		noBudgets: 'common.emptyState.noBudgets',
		noCategories: 'common.emptyState.noCategories',
		noWallets: 'common.emptyState.noWallets',
		noResults: 'common.emptyState.noResults'
	};
	
	$: emoji = customEmoji || emojiMap[type] || '📊';
	$: message = customMessage || t(messageMap[type] || 'common.emptyState.noData');
</script>

<div class="empty-state">
	<h1>{emoji}</h1>
	<p>{message}</p>
</div>

<style>
	.empty-state {
		padding: 30px;
		text-align: center;
		color: var(--color-text);
	}

	.empty-state h1 {
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	.empty-state p {
		font-size: 1.1rem;
		opacity: 0.8;
	}
</style>
