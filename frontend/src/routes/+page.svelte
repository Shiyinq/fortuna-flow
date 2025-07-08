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
		<Card showGradient={true} marginTop={'0px'} marginBottom={'0px'} highlightTitle={true} padding={"0px"}>
			<div class="budget-summary-amount">Total balance</div>
			<div class="budget-summary-value">{formatCurrency(data.balance?.totalBalance || 0)}</div>
		</Card>

		<MyWallets wallets={data.wallets?.data || []}  padding={"16px"}/>

		<Card title="Recent total spends" showGradient={true} marginTop={'0px'} marginBottom={'0px'} highlightTitle={true} padding={"16px"}>
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
		text-align: center;
	}
	.budget-summary-value {
		color: var(--color-theme-1, #00e6b8);
		font-size: 2.2rem;
		font-weight: 700;
		text-align: center;
	}
</style>
