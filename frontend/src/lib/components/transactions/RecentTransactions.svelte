<script lang="ts">
	import { formatCurrency, formatDate } from '$lib/utils';
	import TransactionsInfo from './TransactionsInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import Card from '$lib/components/Card.svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import { currentLanguage, translations } from '$lib/store';

	export let transactions: any;
	const { t } = useTranslation();
</script>

<Card
	title={$t('transactions.recentTransactions')}
	subtitle={$t('transactions.seeAll')}
	subtitleLink="/transactions"
	showGradient={true}
	highlightTitle={true}
	padding={"16px"}
>
	{#if !transactions?.length}
		<EmptyState type="noTransactions" />
	{/if}
	{#each transactions || [] as transaction}
		<TransactionsInfo
			transactionId={transaction.transactionId}
			walletId={transaction.walletId}
			categoryId={transaction.categoryId}
			icon={transaction.categoryIcon}
			category={transaction.categoryName}
			description={formatDate(transaction.transactionDate, $currentLanguage, $translations)}
			note={transaction.note}
			amount={formatCurrency(transaction.amount)}
			type={transaction.type}
			transactionDate={transaction.transactionDate}
		/>
	{/each}
</Card>
