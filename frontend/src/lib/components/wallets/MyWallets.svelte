<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import WalletInfo from './WalletInfo.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import Card from '$lib/components/Card.svelte';

	export let wallets: any;
</script>

<Card title="My Wallets" subtitle="See all" subtitleLink="/wallets" showGradient={true}>
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
