<script>
	import { goto } from '$app/navigation';
	import wallet from '$lib/images/wallet.svg';
	import { transactionSelected } from '$lib/store';
	
    export let transactionId = '';
	export let walletId = '';
	export let categoryId = '';
	export let icon = wallet;
	export let category = '';
	export let description = '';
	export let amount = '0';
	export let type = 'expense';
	export let transactionDate = '';


	$: icon = icon ?? wallet;

	const updateTransaction = () => {
		let data = {
			transactionId,
			walletId,
			categoryId,
			type,
			amount,
			note: description,
			transactionDate
		}
		transactionSelected.set(data);
		goto("/transactions/create");
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div on:click={updateTransaction} class="update-transaction">
	<div class="transactions-info">
		<div class="transactions-title">
			<img class="img-transactions" src={icon} alt="Icon" />
			<div class="transactions-content">
				<p class="category">{category}</p>
				<p class="description">{description}</p>
			</div>
		</div>
		<div class={'transactions-amount ' + type + '-color'}>
			<span>{amount}</span>
		</div>
	</div>
</div>

<style>
	.update-transaction {
		cursor: pointer;
	}

	.transactions-info {
		width: 100%;
		padding: 12px;
		display: flex;
		align-items: center;
		background-color: #fff;
		justify-content: space-between;
		border-bottom: 1px solid var(--color-bg-0);
	}

	.transactions-title {
		gap: 0.4rem;
		display: flex;
		justify-content: center;
		align-items: center;
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
		font-size: 13px;
		font-weight: bold;
	}

	.description {
		padding: 0;
		margin: 0;
		font-size: 12px;
	}

	img {
		width: 1em;
		height: 1em;
		margin-right: 8px;
		object-fit: contain;
	}
</style>
