<script lang="ts">
	import { formatCurrency, formatDate } from '$lib/utils';
	import TransactionsInfo from './TransactionsInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

	export let transactions: any;
</script>

<div class="recent-transactions">
	<div class="recent-transactions-header">
		<h5>Recent transactions</h5>
		<a href="/transactions"><h6>See all</h6></a>
	</div>
	{#if !transactions.length}
		<EmptyState />
	{/if}
	{#each transactions as transaction}
		<TransactionsInfo
			transactionId={transaction.transactionId}
			walletId={transaction.walletId}
			categoryId={transaction.categoryId}
			icon={transaction.categoryIcon}
			category={transaction.categoryName}
			description={formatDate(transaction.transactionDate)}
			note={transaction.note}
			amount={formatCurrency(transaction.amount)}
			type={transaction.type}
			transactionDate={transaction.transactionDate}
		/>
	{/each}
</div>

<style>
	h5,
	h6 {
		margin-top: 0;
	}

	.recent-transactions {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	.recent-transactions-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}
</style>
