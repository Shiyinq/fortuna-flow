<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import WalletInfo from './WalletInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let wallets: any;
	export let title: string = 'My Wallets';
	export let subtitle: string = 'See all';
	export let subtitleLink: string = '/wallets';
	export let showGradient: boolean = true;
	export let padding: string = '20px';
	export let marginBottom: string = '16px';
	export let marginTop: string = '16px';
</script>

<Card {title} {subtitle} {subtitleLink} {showGradient} {padding} {marginBottom} {marginTop} highlightTitle={true}>
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
</Card>
