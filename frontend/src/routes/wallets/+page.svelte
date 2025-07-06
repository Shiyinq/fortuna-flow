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
	<div class="wallets">
		<LoadingState message="Please wait while we load your wallets." />
	</div>
{/if}

<style>
	.wallets {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		position: relative;
		overflow: hidden;
	}
</style>
