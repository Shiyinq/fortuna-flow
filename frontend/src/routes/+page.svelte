<script lang="ts">
	import { formatCurrency } from '$lib/utils';

	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import StackedBarChart from '$lib/components/charts/StackedBarChart.svelte';
	import RecentTransactions from '$lib/components/transactions/RecentTransactions.svelte';

	export let data: any;

	let recentTotalSpends = {
		month: [ 'March', 'April', 'May', 'June'],
		data: {
			income: [0, 1000000, 2000000, 1200000],
			expense: [-1000000, -500000, -1200000, -800000]
		}
	};
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Fortuna Flow" />
</svelte:head>

<div class="home">
	<div class="total-balance">
		<h3>{formatCurrency(data.balance.totalBalance)}</h3>
		<span>Total balance</span>
	</div>

	<br />

	<MyWallets wallets={data.wallets.data} />

	<br />
	<div class="total-spend">
		<div class="total-spend-header">
			<h5>Recent total spends</h5>
		</div>
		<StackedBarChart data={recentTotalSpends}/>
	</div>

	<br />

	<RecentTransactions transactions={data.recent} />
</div>

<style>
	.home {
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.total-balance {
		width: 100%;
	}

	.total-spend {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	h3 {
		padding: 0;
		margin: 0;
	}

	h5 {
		margin-top: 0;
	}

	span {
		font-size: 13px;
	}
</style>
