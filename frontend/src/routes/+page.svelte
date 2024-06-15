<script>
	import BarChart from '$lib/components/charts/BarChart.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import RecentTransactions from '$lib/components/transactions/RecentTransactions.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Fortuna Flow" />
</svelte:head>

<div class="home">
	<div class="total-balance">
		<h3>Rp 1.429.732,42</h3>
		<span>Total balance</span>
	</div>

	<br />

	<MyWallets />

	<br />

	<div class="total-spent">
		<div class="total-spent-header">
			<h5>Recent total spents</h5>
		</div>
		<BarChart />
	</div>

	<br />

	<RecentTransactions />
</div>

<style>
	.home {
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.total-balance {
		width: 320px;
	}

	.total-spent {
		width: 320px;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.7);
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
