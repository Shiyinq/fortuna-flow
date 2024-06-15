<script>
	import wallet from '$lib/images/wallet.svg';
	export let icon = wallet;
	export let category = '';
	export let description = '';
	export let amount = '0';
	export let type = 'expense';
</script>

<div class="transactions-info">
	<div class="transactions-title">
		<img class="img-transactions" src={icon} alt="Icon" />
		<div class="transactions-content">
			<p class="category">{category}</p>
			<p class="description">{description}</p>
		</div>
	</div>
	<div class={'transactions-amount ' + type + '-color'}>
		<span>Rp {amount}</span>
	</div>
</div>

<style>
	.transactions-info {
		width: 100%;
		padding: 12px;
		display: flex;
		border-bottom: 2px solid #fff;
		justify-content: space-between;
		align-items: center;
		background-color: rgba(255, 255, 255, 0.7);
	}

	.transactions-title {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 0.4rem;
	}

	.transactions-amount {
		font-size: 12px;
	}

	.expense-color {
		color: #ff4c4c;
	}

	.income-color {
		color: #4caf50;
	}

	.category {
		padding: 0;
		margin: 0;
		font-weight: bold;
		font-size: 13px;
	}

	.description {
		padding: 0;
		margin: 0;
		font-size: 12px;
	}

	img {
		width: 1em;
		height: 1em;
		object-fit: contain;
		margin-right: 8px;
	}
</style>
