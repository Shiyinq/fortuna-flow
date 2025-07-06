<script lang="ts">
	import { onMount } from 'svelte';
	import { activeMonth, activeWallet, currentTransaction, token, wallets } from '$lib/store';
	import { formatCurrency, formatDate } from '$lib/utils';

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
		if (data) {
			wallets.set(data.listWallet || []);
			activeTransactions = data.transactions?.data ?? [];
			currentTransaction.set(activeTransactions);
		}
	});
</script>

<svelte:head>
	<title>Transactions</title>
	<meta name="description" content="Fortuna Flow - Transactions" />
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
			<EmptyState />
		{/if}
		{#each activeTransactions as { transactionDate, transactions, totalAmountExpense, totalAmountIncome }}
			<Card marginBottom={"0"} marginTop={"0"} padding={"1px"} showGradient={true}>
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
			</Card>
			<br />
		{/each}

		<FloatingButton />
	</div>
{:else}
	<div class="transactions">
		<LoadingState message="Please wait while we load your transactions." />
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
		color: #222;
	}

	.transactions-header h5 {
		font-size: 1.05rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}
</style>
