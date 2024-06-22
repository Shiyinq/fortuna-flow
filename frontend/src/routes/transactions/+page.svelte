<script lang="ts">
	import { onMount } from 'svelte';
	import { activeMonth, activeWallet, token, wallets } from '$lib/store';
	import { formatCurrency, formatDate, getCurrentMonth } from '$lib/utils';

	import { getWalletTransactions } from '$lib/apis/wallets';
	import { getAllTransactions } from '$lib/apis/transactions';

	import EmptyState from '$lib/components/EmptyState.svelte';
	import CurrentWallet from '$lib/components/wallets/CurrentWallet.svelte';
	import MonthSelector from '$lib/components/transactions/MonthSelector.svelte';
	import TransactionsInfo from '$lib/components/transactions/TransactionsInfo.svelte';
	import TransactionsRecap from '$lib/components/transactions/TransactionsRecap.svelte';

	export let data: any;

	let activeTransactions: any = [];

	const getTransactionsSelectedWallet = async () => {
		try {
			let walletId = $activeWallet.walletId;

			if (walletId == 'all') {
				let { metadata, data } = await getAllTransactions($token, 1, 32, $activeMonth);
				activeTransactions = data ?? [];
			} else {
				let { metadata, data } = await getWalletTransactions($token, walletId, $activeMonth);
				activeTransactions = data ?? [];
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
					icon={transaction.categoryDetail.categoryIcon}
					category={transaction.categoryDetail.name}
					description={transaction.note}
					amount={formatCurrency(transaction.amount)}
					type={transaction.type}
				/>
			{/each}
		</div>
		<br />
	{/each}
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
