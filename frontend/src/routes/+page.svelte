<script lang="ts">
	import { formatCurrency } from '$lib/utils';

	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import StackedBarChart from '$lib/components/charts/StackedBarChart.svelte';
	import RecentTransactions from '$lib/components/transactions/RecentTransactions.svelte';
	import FloatingButton from '$lib/components/FloatingButton.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let data: any;
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Fortuna Flow" />
</svelte:head>

{#if data}
	<div class="home">
		<Card showGradient={true} marginTop={'0px'} marginBottom={'0px'} highlightTitle={true}>
			<div class="budget-summary-amount">Total balance</div>
			<div class="budget-summary-value">{formatCurrency(data.balance?.totalBalance || 0)}</div>
		</Card>

		<MyWallets wallets={data.wallets?.data || []} />

		<Card title="Recent total spends" showGradient={true} marginTop={'0px'} marginBottom={'0px'} highlightTitle={true}>
			<StackedBarChart data={data.recentTotalTransactions || []} />
		</Card>

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

	.budget-summary-amount {
		color: #aaa;
		font-size: 1.1rem;
		margin-bottom: 8px;
		text-align: center;
	}
	.budget-summary-value {
		color: var(--color-theme-1, #00e6b8);
		font-size: 2.2rem;
		font-weight: 700;
		margin-bottom: 18px;
		text-align: center;
	}

	.balance-amount {
		text-align: center;
		margin-top: -24px;
		margin-bottom: -24px;
	}

	.balance-amount h3.text-balance {
		color: var(--color-theme-1, #00e6b8);
		text-align: center;
		padding: 0;
		margin: 0;
		font-size: 2.2rem;
		font-weight: 700;
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		letter-spacing: -0.5px;
	}
</style>
