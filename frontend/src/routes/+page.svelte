<script lang="ts">
	import BarChart from '$lib/components/charts/BarChart.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import RecentTransactions from '$lib/components/transactions/RecentTransactions.svelte';
	import { formatCurrency } from '$lib/utils';

	export let data: any;
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

	<div class="total-spent">
		<div class="total-spent-header">
			<h5>Recent total spents</h5>
		</div>
		<BarChart />
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

	.total-spent {
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
