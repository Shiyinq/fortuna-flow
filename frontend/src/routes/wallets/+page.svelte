<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let data: any;
</script>

{#if data}
	<Card title="My Wallets" subtitle="Create New Wallet" subtitleLink="/wallets/create" showGradient={true}>
		{#if !data.wallets?.data?.length}
			<EmptyState />
		{/if}
		{#each data.wallets?.data || [] as wallet}
			<WalletInfo
				icon={wallet.walletIcon}
				title={wallet.name}
				balance={formatCurrency(wallet.balance)}
			/>
		{/each}
	</Card>
{:else}
	<div class="wallets glassy">
		<LoadingState message="Please wait while we load your wallets." />
	</div>
{/if}

<style>
	.wallets {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		position: relative;
		overflow: hidden;
	}
</style>
