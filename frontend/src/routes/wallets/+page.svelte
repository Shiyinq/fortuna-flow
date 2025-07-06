<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';

	export let data: any;
</script>

{#if data}
	<div class="wallets">
		<div class="wallet-header">
			<h5>My Wallets</h5>
			<a href="/wallets/create"><h6>Create New Wallet</h6></a>
		</div>
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
	</div>
{:else}
	<div class="wallets">
		<LoadingState message="Please wait while we load your wallets." />
	</div>
{/if}

<style>
	h5,
	h6 {
		margin-top: 0;
	}
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

	.wallet-header {
		width: 100%;
		display: flex;
		margin-bottom: 16px;
		justify-content: space-between;
		align-items: center;
		position: relative;
		z-index: 1;
	}

	.wallet-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.wallet-header h6 {
		font-size: 0.9rem;
		font-weight: 500;
		margin: 0;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

</style>
