<script>
	import wallet from '$lib/images/wallet.svg';
	import WalletInfo from './WalletInfo.svelte';

	let wallets = [
		{
			icon: wallet,
			title: 'ATM',
			balance: '10.200.000'
		},
		{
			icon: wallet,
			title: 'E-wallet',
			balance: '598.352,42'
		},
		{
			icon: wallet,
			title: 'Cash',
			balance: '100.000'
		}
	];
</script>

<div class="wallets">
	<div class="wallet-header">
		<h5>My Wallets</h5>
		<a href="/wallets"><h6>See all</h6></a>
	</div>
	{#each wallets as wallet}
		<WalletInfo icon={wallet.icon} title={wallet.title} balance={wallet.balance} />
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
