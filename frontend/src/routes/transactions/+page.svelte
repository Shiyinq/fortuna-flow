<script>
	import wallet from '$lib/images/wallet.svg';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';
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

	let currentWallet = {
		icon: wallet,
		title: 'ATM',
		balance: '10.200.000'
	};
</script>

<div class="transactions">
	<div class="current-wallet">
		<div class="change-wallet">
			<h5>Wallet</h5>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#"><h6>Change</h6></a>
		</div>
		<WalletInfo
			icon={currentWallet.icon}
			title={currentWallet.title}
			balance={currentWallet.balance}
		/>
	</div>
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
		margin-top: 24px;
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	h5,
	h6 {
		margin-top: 0;
		margin-bottom: 0;
	}

	.transactions-card {
		width: 320px;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	.change-wallet,
	.transactions-header {
		width: 300px;
		display: flex;
		margin-top: 8px;
		margin-bottom: 4px;
		justify-content: space-between;
	}
</style>
