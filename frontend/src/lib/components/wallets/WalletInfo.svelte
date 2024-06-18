<script>
	import wallet from '$lib/images/wallet.svg';

	export let icon = wallet;
	export let title = '';
	export let balance = '0';

	const defaultIcon = wallet;

	$: icon = icon ?? defaultIcon;
</script>

<div class="wallet-info">
	<div class="wallet-title">
		<img class="img-wallet" src={icon} alt="Icon" />
		<span>{title}</span>
	</div>
	<div class="wallet-balance">
		<span>{balance}</span>
	</div>
</div>

<style>
	.wallet-info {
		width: 100%;
		padding: 12px;
		display: flex;
		border-radius: 8px;
		margin-bottom: 8px;
		justify-content: space-between;
		background-color: rgba(255, 255, 255, 0.7);
	}

	.wallet-title {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 0.4rem;
	}

	span {
		font-size: 13px;
	}

	img {
		width: 1em;
		height: 1em;
		object-fit: contain;
		margin-right: 8px;
	}
</style>
