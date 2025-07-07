<script>
	import wallet from '$lib/images/wallet.svg';
	import IconDisplay from '$lib/components/IconDisplay.svelte';
	import CardItem from '$lib/components/CardItem.svelte';

	export let icon = wallet;
	export let title = '';
	export let balance = '0';

	const defaultIcon = wallet;

	$: icon = icon ?? defaultIcon;
</script>

<CardItem
	iconComponent={IconDisplay}
	{icon}
	iconProps={{ icon, alt: 'Wallet Icon' }}
	{title}
	amount={balance}
	type="neutral"
/>
