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
	{#if !wallets?.length}
		<EmptyState />
	{/if}
	{#each wallets || [] as wallet}
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

	.wallets::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
		pointer-events: none;
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
