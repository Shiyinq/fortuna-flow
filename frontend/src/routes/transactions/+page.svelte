<script lang="ts">
	import wallet from '$lib/images/wallet.svg';
	import CurrentWallet from '$lib/components/wallets/CurrentWallet.svelte';
	import MonthSelector from '$lib/components/transactions/MonthSelector.svelte';
	import TransactionsInfo from '$lib/components/transactions/TransactionsInfo.svelte';

	let transactions = [
		{
			transactionDate: '2024-06-15',
			datas: [
				{
					icon: wallet,
					category: 'Transportation',
					description: 'Ojol',
					date: 'Sat, 15 June 2024',
					amount: '220.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-14',
			datas: [
				{
					icon: wallet,
					category: 'Food',
					description: 'Makan siang',
					date: 'Fri, 14 June 2024',
					amount: '120.352',
					type: 'expense'
				},
				{
					icon: wallet,
					category: 'Gift',
					description: 'Hadiah',
					date: 'Fri, 14 June 2024',
					amount: '520.000',
					type: 'income'
				}
			]
		},
		{
			transactionDate: '2024-06-13',
			datas: [
				{
					icon: wallet,
					category: 'Self Care',
					description: 'Skin care',
					date: 'Thu, 13 June 2024',
					amount: '560.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-12',
			datas: [
				{
					icon: wallet,
					category: 'Utilities',
					description: 'Electricity Bill',
					date: 'Wed, 12 June 2024',
					amount: '300.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-11',
			datas: [
				{
					icon: wallet,
					category: 'Entertainment',
					description: 'Movie Ticket',
					date: 'Tue, 11 June 2024',
					amount: '150.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-10',
			datas: [
				{
					icon: wallet,
					category: 'Food',
					description: 'Groceries',
					date: 'Mon, 10 June 2024',
					amount: '450.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-09',
			datas: [
				{
					icon: wallet,
					category: 'Health',
					description: 'Doctor Appointment',
					date: 'Sun, 09 June 2024',
					amount: '700.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-08',
			datas: [
				{
					icon: wallet,
					category: 'Income',
					description: 'Salary',
					date: 'Sat, 08 June 2024',
					amount: '5000.000',
					type: 'income'
				}
			]
		},
		{
			transactionDate: '2024-06-07',
			datas: [
				{
					icon: wallet,
					category: 'Transportation',
					description: 'Taxi',
					date: 'Fri, 07 June 2024',
					amount: '200.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-06',
			datas: [
				{
					icon: wallet,
					category: 'Self Care',
					description: 'Massage',
					date: 'Thu, 06 June 2024',
					amount: '300.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-05',
			datas: [
				{
					icon: wallet,
					category: 'Food',
					description: 'Dinner',
					date: 'Wed, 05 June 2024',
					amount: '250.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-04',
			datas: [
				{
					icon: wallet,
					category: 'Utilities',
					description: 'Water Bill',
					date: 'Tue, 04 June 2024',
					amount: '100.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-03',
			datas: [
				{
					icon: wallet,
					category: 'Transportation',
					description: 'Train Ticket',
					date: 'Mon, 03 June 2024',
					amount: '75.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-02',
			datas: [
				{
					icon: wallet,
					category: 'Food',
					description: 'Lunch',
					date: 'Sun, 02 June 2024',
					amount: '125.000',
					type: 'expense'
				}
			]
		},
		{
			transactionDate: '2024-06-01',
			datas: [
				{
					icon: wallet,
					category: 'Gift',
					description: 'Birthday Gift',
					date: 'Sat, 01 June 2024',
					amount: '400.000',
					type: 'expense'
				}
			]
		}
	];
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
	{#each transactions as { transactionDate, datas }}
		<div class="transactions-card">
			<div class="transactions-header">
				<h5>{transactionDate}</h5>
				<!-- <a href="/recent-transactions"><h6>See all</h6></a> -->
			</div>
			{#each datas as data}
				<TransactionsInfo
					icon={data.icon}
					category={data.category}
					description={data.description}
					amount={data.amount}
					type={data.type}
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
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	.transactions-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		margin-bottom: 4px;
		justify-content: space-between;
	}
</style>
