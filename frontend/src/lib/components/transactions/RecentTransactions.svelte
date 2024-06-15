<script>
	import wallet from '$lib/images/wallet.svg';
	import TransactionsInfo from './TransactionsInfo.svelte';

	let transactions = [
		{
			icon: wallet,
			category: 'Transportation',
			description: 'Ojol',
			date: 'Sat, 15 June 2024',
			amount: '220.000',
			type: 'expense'
		},
		{
			icon: wallet,
			category: 'Food',
			description: 'Makan siang',
			date: 'Sat, 15 June 2024',
			amount: '120.352',
			type: 'expense'
		},
		{
			icon: wallet,
			category: 'Gift',
			description: 'Hadia',
			date: 'Sat, 15 June 2024',
			amount: '520.000',
			type: 'income'
		},
		{
			icon: wallet,
			category: 'Self Care',
			description: 'Skin care',
			date: 'Sat, 15 June 2024',
			amount: '560.000',
			type: 'expense'
		}
	];
</script>

<div class="recent-transactions">
	<div class="recent-transactions-header">
		<h5>Recent transactions</h5>
		<a href="/recent-transactions"><h6>See all</h6></a>
	</div>

	{#each transactions as transaction}
		<TransactionsInfo
			icon={transaction.icon}
			category={transaction.category}
			description={transaction.date}
			amount={transaction.amount}
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
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	.recent-transactions-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}
</style>
