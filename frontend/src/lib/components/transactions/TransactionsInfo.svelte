<script>
	import { goto } from '$app/navigation';
	import wallet from '$lib/images/wallet.svg';
	import { transactionSelected } from '$lib/store';
	import IconDisplay from '$lib/components/IconDisplay.svelte';
	import CardItem from '$lib/components/CardItem.svelte';

	export let transactionId = '';
	export let walletId = '';
	export let categoryId = '';
	export let icon = wallet;
	export let category = '';
	export let description = '';
	export let note = '';
	export let amount = '';
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

<CardItem
	iconComponent={IconDisplay}
	{icon}
	iconProps={{ icon, alt: 'Transaction Icon' }}
	title={category}
	subtitle={description}
	{amount}
	{type}
	onClick={updateTransaction}
	highlightTitle={true}
	highlightAmount={true}
/>
