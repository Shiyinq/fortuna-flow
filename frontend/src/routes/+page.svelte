<script lang="ts">
	import { formatCurrency } from '$lib/utils';

	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import StackedBarChart from '$lib/components/charts/StackedBarChart.svelte';
	import RecentTransactions from '$lib/components/transactions/RecentTransactions.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';

	export let data: any;
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Fortuna Flow" />
</svelte:head>

{#if data}
	<div class="home">
		<div class="total-balance">
			<div class="total-balance-header">
				<h5>Total balance</h5>
			</div>
			<div class="balance-amount">
				<h3>{formatCurrency(data.balance?.totalBalance || 0)}</h3>
			</div>
		</div>

		<MyWallets wallets={data.wallets?.data || []} />

		<div class="total-spend">
			<div class="total-spend-header">
				<h5>Recent total spends</h5>
			</div>
			<StackedBarChart data={data.recentTotalTransactions || []} />
		</div>

		<RecentTransactions transactions={data.recent || []} />
		<FloatingButton />
	</div>
{:else}
	<div class="home">
		<LoadingState message="Please wait while we load your data." />
	</div>
{/if}

<style>
	.home {
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.total-spend {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		position: relative;
		overflow: hidden;
	}

	.total-spend::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255,255,255,0.12) 0%, transparent 50%, rgba(255,255,255,0.12) 100%);
		pointer-events: none;
	}

	.total-spend-header {
		margin-bottom: 16px;
		position: relative;
		z-index: 1;
	}

	.total-spend-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.total-spend :global(.chart-container) {
		position: relative;
		z-index: 1;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 16px;
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	.total-balance {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		/* margin-bottom: 12px; */
		position: relative;
		overflow: hidden;
	}

	.total-balance::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
		pointer-events: none;
	}

	.total-balance-header {
		margin-bottom: 16px;
		position: relative;
		z-index: 1;
	}

	.total-balance-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.balance-amount {
		text-align: center;
		position: relative;
		z-index: 1;
	}

	.balance-amount h3 {
		padding: 0;
		margin: 0;
		font-size: 2.5rem;
		font-weight: 700;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		letter-spacing: -0.5px;
	}


</style>
