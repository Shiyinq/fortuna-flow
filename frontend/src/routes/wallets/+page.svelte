<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';

	export let data: any;
</script>

<div class="wallets">
	<div class="wallet-header">
		<h5>My Wallets</h5>
		<a href="/wallets"><h6>Create New Wallet</h6></a>
	</div>
	{#each data.wallets.data as wallet}
		<WalletInfo icon={wallet.walletIcon} title={wallet.name} balance={formatCurrency(wallet.balance)} />
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
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	.wallet-header {
		width: 100%;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}
</style>
