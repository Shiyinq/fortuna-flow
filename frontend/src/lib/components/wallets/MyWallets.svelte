<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import WalletInfo from './WalletInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

	export let wallets: any;
</script>

<div class="wallets">
	<div class="wallet-header">
		<h5>My Wallets</h5>
		<a href="/wallets"><h6>See all</h6></a>
	</div>
	{#if !wallets.length}
		<EmptyState />
	{/if}
	{#each wallets as wallet}
		<WalletInfo
			icon={wallet.walletIcon}
			title={wallet.name}
			balance={formatCurrency(wallet.balance)}
		/>
	{/each}
</div>

<style>
	h5,
	h6 {
		margin-top: 0;
	}
	.wallets {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	.wallet-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}
</style>
