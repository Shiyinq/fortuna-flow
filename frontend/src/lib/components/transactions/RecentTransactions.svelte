<script lang="ts">
	import { formatCurrency, formatDate } from '$lib/utils';
	import TransactionsInfo from './TransactionsInfo.svelte';

	export let transactions: any;
</script>

<div class="recent-transactions">
	<div class="recent-transactions-header">
		<h5>Recent transactions</h5>
		<a href="/transactions"><h6>See all</h6></a>
	</div>

	{#each transactions as transaction}
		<TransactionsInfo
			icon={transaction.categoryIcon}
			category={transaction.categoryName}
			description={formatDate(transaction.transactionDate)}
			amount={formatCurrency(transaction.amount)}
			type={transaction.type}
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
