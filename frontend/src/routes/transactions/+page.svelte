<script lang="ts">
	import { onMount } from 'svelte';
	import { activeMonth, activeWallet, currentTransaction, token, wallets, currentLanguage, translations } from '$lib/store';
	import { formatCurrency, formatDate } from '$lib/utils';
	import { useTranslation } from '$lib/i18n/useTranslation';

	import { getWalletTransactions } from '$lib/apis/wallets';
	import { getAllTransactions } from '$lib/apis/transactions';

	import EmptyState from '$lib/components/EmptyState.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';
	import CurrentWallet from '$lib/components/wallets/CurrentWallet.svelte';
	import MonthSelector from '$lib/components/transactions/MonthSelector.svelte';
	import TransactionsInfo from '$lib/components/transactions/TransactionsInfo.svelte';
	import TransactionsRecap from '$lib/components/transactions/TransactionsRecap.svelte';
	import AddTransactionButton from '$lib/components/transactions/AddTransactionButton.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';

	const { t } = useTranslation();

	export let data: any;

	let activeTransactions: any = [];

	const getTransactionsSelectedWallet = async () => {
		try {
			const selectedWallet = $wallets[$activeWallet];
			if (!selectedWallet) {
				activeTransactions = [];
				currentTransaction.set([]);
				return;
			}
			let walletId = selectedWallet.walletId;

			if (walletId == 'all') {
				let { metadata, data } = await getAllTransactions($token, 1, 32, $activeMonth);
				activeTransactions = data ?? [];
				currentTransaction.set(activeTransactions);
			} else {
				let { metadata, data } = await getWalletTransactions($token, walletId, $activeMonth);
				activeTransactions = data ?? [];
				currentTransaction.set(activeTransactions);
			}
		} catch (error) {
			console.log(error);
		}
	};

	$: if ($activeWallet || $activeMonth) {
		getTransactionsSelectedWallet();
	}

	onMount(() => {
		if (data) {
			wallets.set(data.listWallet || []);
			activeTransactions = data.transactions?.data ?? [];
			currentTransaction.set(activeTransactions);
		}
	});

	// Update "All Wallets" name when language changes
	$: if ($wallets.length > 0 && $wallets[0]?.walletId === 'all') {
		$wallets[0].name = $t('wallets.allWallets');
	}
</script>

<svelte:head>
	<title>{$t('transactions.title')}</title>
	<meta name="description" content="Fortuna Flow - {$t('transactions.title')}" />
</svelte:head>

{#if data}
	<div class="transactions">
		<CurrentWallet />
		<br />
		<MonthSelector />
		<br />
		<TransactionsRecap transactions={activeTransactions} />
		<br />
		<AddTransactionButton />
		{#if !activeTransactions.length}
			<EmptyState type="noTransactions" />
		{/if}
		{#each activeTransactions as { transactionDate, transactions, totalAmountExpense, totalAmountIncome }}
			<Card marginBottom={'0'} marginTop={'0'} padding={'1px'} showGradient={true}>
				<div class="transactions-header">
					<span class="budget-group-title">{formatDate(transactionDate, $currentLanguage, $translations)}</span>
					<span class="budget-group-total">{formatCurrency(totalAmountIncome - totalAmountExpense)}</span>
				</div>
				{#each transactions as transaction}
					<TransactionsInfo
						transactionId={transaction.transactionId}
						walletId={transaction.walletId}
						categoryId={transaction.categoryId}
						icon={transaction.categoryDetail.categoryIcon}
						category={transaction.categoryDetail.name}
						description={transaction.note}
						note={transaction.note}
						amount={formatCurrency(transaction.amount)}
						type={transaction.type}
						{transactionDate}
					/>
				{/each}
			</Card>
			<br />
		{/each}

		<FloatingButton />
	</div>
{:else}
	<div class="transactions">
		<LoadingState message={$t('common.loading')} />
	</div>
{/if}

<style>
	.transactions {
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.transactions-header {
		width: 100%;
		display: flex;
		margin-bottom: 6px;
		justify-content: space-between;
		align-items: center;
	}

	.budget-group-title {
		font-weight: 600;
		font-size: 1.1rem;
		color: var(--color-theme-1);
	}
	.budget-group-total {
		font-size: 0.95rem;
		color: var(--color-text-muted);
	}
</style>
