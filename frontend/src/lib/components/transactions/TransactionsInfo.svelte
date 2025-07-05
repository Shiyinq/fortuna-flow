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
	export let note = '';
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
			note,
			transactionDate
		};
		transactionSelected.set(data);
		goto('/transactions/create');
	};
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
		padding: 16px;
		display: flex;
		align-items: center;
		background: rgba(44,62,80,0.08);
		border: 1px solid rgba(44,62,80,0.10);
		border-radius: 12px;
		margin-bottom: 12px;
		justify-content: space-between;
		position: relative;
		z-index: 1;
		transition: all 0.3s ease;
	}

	.transactions-info:hover {
		background: rgba(44,62,80,0.13);
		transform: translateY(-2px);
		box-shadow: 0 4px 16px rgba(44,62,80,0.08);
	}

	.transactions-title {
		gap: 0.4rem;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.transactions-amount {
		font-size: 14px;
		font-weight: 600;
		color: #222;
	}

	.expense-color {
		color: #ff6b6b;
	}

	.income-color {
		color: #51cf66;
	}

	.category {
		padding: 0;
		margin: 0;
		font-size: 14px;
		font-weight: 600;
		color: #222;
	}

	.description {
		padding: 0;
		margin: 0;
		font-size: 12px;
		color: #555;
	}

	img {
		width: 1.2em;
		height: 1.2em;
		margin-right: 8px;
		object-fit: contain;
		filter: none;
	}
</style>
