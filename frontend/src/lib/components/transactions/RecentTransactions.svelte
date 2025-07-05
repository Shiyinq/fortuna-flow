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
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		position: relative;
		overflow: hidden;
	}

	.recent-transactions::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
		pointer-events: none;
	}

	.recent-transactions-header {
		width: 100%;
		display: flex;
		margin-bottom: 16px;
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
	}

	.recent-transactions-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.recent-transactions-header h6 {
		font-size: 0.9rem;
		font-weight: 500;
		margin: 0;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}
</style>
