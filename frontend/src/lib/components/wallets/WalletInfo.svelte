<script>
	import wallet from '$lib/images/wallet.svg';
	import IconDisplay from '$lib/components/IconDisplay.svelte';

	export let icon = wallet;
	export let title = '';
	export let balance = '0';

	const defaultIcon = wallet;

	$: icon = icon ?? defaultIcon;
</script>

<div class="wallet-info">
	<div class="wallet-title">
		<IconDisplay icon={icon} alt="Wallet Icon" />
		<span>{title}</span>
	</div>
	<div class="wallet-balance">
		<span>{balance}</span>
	</div>
</div>

<style>
	.wallet-info {
		width: 100%;
		padding: 16px;
		display: flex;
		border-radius: 12px;
		margin-bottom: 12px;
		background: rgba(44,62,80,0.08);
		border: 1px solid rgba(44,62,80,0.10);
		justify-content: space-between;
		position: relative;
		z-index: 1;
		transition: all 0.3s ease;
	}

	.wallet-info:hover {
		background: rgba(44,62,80,0.13);
		transform: translateY(-2px);
		box-shadow: 0 4px 16px rgba(44,62,80,0.08);
	}

	.wallet-title {
		gap: 0.4rem;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.wallet-title span {
		font-size: 14px;
		font-weight: 500;
		color: #222;
	}

	.wallet-balance span {
		font-size: 14px;
		font-weight: 600;
		color: #222;
	}
</style>
