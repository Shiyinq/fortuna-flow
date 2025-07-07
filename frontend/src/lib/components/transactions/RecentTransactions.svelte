<script lang="ts">
	import { formatCurrency, formatDate } from '$lib/utils';
	import TransactionsInfo from './TransactionsInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let transactions: any;
</script>

<Card
	title="Recent transactions"
	subtitle="See all"
	subtitleLink="/transactions"
	showGradient={true}
	highlightTitle={true}
>
	{#if !transactions?.length}
		<EmptyState />
	{/if}
	{#each transactions || [] as transaction}
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
</Card>
