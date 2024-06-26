<script lang="ts">
	import { onMount } from 'svelte';
	import { activeMonth, activeWallet, currentTransaction, token, wallets } from '$lib/store';
	import { formatCurrency, formatDate, getCurrentMonth } from '$lib/utils';

	import { getWalletTransactions } from '$lib/apis/wallets';
	import { getAllTransactions } from '$lib/apis/transactions';

	import EmptyState from '$lib/components/EmptyState.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';
	import CurrentWallet from '$lib/components/wallets/CurrentWallet.svelte';
	import MonthSelector from '$lib/components/transactions/MonthSelector.svelte';
	import TransactionsInfo from '$lib/components/transactions/TransactionsInfo.svelte';
	import TransactionsRecap from '$lib/components/transactions/TransactionsRecap.svelte';
	import AddTransactionButton from '$lib/components/transactions/AddTransactionButton.svelte';

	export let data: any;

	let activeTransactions: any = [];

	const getTransactionsSelectedWallet = async () => {
		try {
			let walletId = $wallets[$activeWallet].walletId;

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
		wallets.set(data.listWallet);
		activeTransactions = data.transactions.data ?? [];
		currentTransaction.set(activeTransactions);
	});
</script>

<svelte:head>
	<title>Transactions</title>
	<meta name="description" content="Fortuna Flow - Transactions" />
</svelte:head>

<div class="transactions">
	<CurrentWallet />
	<br />
	<MonthSelector />
	<br />
	<TransactionsRecap transactions={activeTransactions} />
	<br />
	<AddTransactionButton />
	{#if !activeTransactions.length}
		<EmptyState />
	{/if}
	{#each activeTransactions as { transactionDate, transactions, totalAmountExpense, totalAmountIncome }}
		<div class="transactions-card">
			<div class="transactions-header">
				<h5>{formatDate(transactionDate)}</h5>
				<h5>{formatCurrency(totalAmountIncome - totalAmountExpense)}</h5>
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
		</div>
		<br />
	{/each}

	<FloatingButton />
</div>

<style>
	.transactions {
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	h5 {
		margin-top: 0;
		margin-bottom: 0;
	}

	.transactions-card {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	.transactions-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		margin-bottom: 4px;
		justify-content: space-between;
	}
</style>
