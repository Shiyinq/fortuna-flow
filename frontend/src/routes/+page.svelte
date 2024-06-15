<script>
	import wallet from '$lib/images/wallet.svg';
	import BarChart from '$lib/components/charts/BarChart.svelte';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Fortuna Flow" />
</svelte:head>

<div class="home">
	<div class="total-balance">
		<h3>Rp 1.429.732,42</h3>
		<span>Total balance</span>
	</div>

	<br />

	<div class="wallets">
		<div class="wallet-header">
			<h5>My Wallets</h5>
			<a href="/wallets"><h6>See all</h6></a>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>ATM</span>
			</div>
			<div class="wallet-balance">
				<span>Rp 298.352,42</span>
			</div>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>E-wallet</span>
			</div>
			<div class="wallet-balance">
				<span>Rp 598.352,42</span>
			</div>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>Cash</span>
			</div>
			<div class="wallet-blance">
				<span>Rp 100.000</span>
			</div>
		</div>
	</div>

	<br />

	<div class="total-spent">
		<div class="total-spent-header">
			<h5>Recent total spents</h5>
		</div>
		<BarChart />
	</div>

	<br />

	<div class="wallets">
		<div class="wallet-header">
			<h5>Recent transactions</h5>
			<a href="/wallets"><h6>See all</h6></a>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>Ojol</span>
			</div>
			<div class="wallet-balance">
				<span>Rp 298.352,42</span>
			</div>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>Makan siang</span>
			</div>
			<div class="wallet-balance">
				<span>Rp 598.352,42</span>
			</div>
		</div>
		<div class="wallet-info">
			<div class="wallet-title">
				<img class="img-google" src={wallet} alt="Google" />
				<span>Beli skin care</span>
			</div>
			<div class="wallet-blance">
				<span>Rp 100.000</span>
			</div>
		</div>
	</div>
</div>

<style>
	.home {
		margin-top: 24px;
		display: flex;
		align-items: center;
		flex-direction: column;
	}

	.total-balance {
		width: 320px;
	}

	.total-spent {
		width: 320px;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	h3 {
		padding: 0;
		margin: 0;
	}
	h5,
	h6 {
		margin-top: 0;
	}
	.wallets {
		width: 320px;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.7);
	}

	.wallet-header {
		width: 300px;
		display: flex;
		margin-top: 8px;
		justify-content: space-between;
	}

	.wallet-info {
		width: 300px;
		padding: 12px;
		display: flex;
		border-radius: 8px;
		margin-bottom: 8px;
		justify-content: space-between;
		background-color: rgba(255, 255, 255, 0.7);
	}

	.wallet-title {
		display: flex;
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
