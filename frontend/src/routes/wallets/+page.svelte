<script lang="ts">
	import LoadingState from '$lib/components/LoadingState.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';

	export let data: any;
</script>

{#if data}
	<MyWallets
		wallets={data.wallets?.data || []}
		title="My Wallets"
		subtitle="New Wallet"
		subtitleLink="/wallets/create"
		showGradient={true}
		marginTop={'0px'}
		marginBottom={'0px'}
	/>
{:else}
	<div class="wallets glassy">
		<LoadingState message="Please wait while we load your wallets." />
	</div>
{/if}

<style>
	.wallets {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		position: relative;
		overflow: hidden;
		background: var(--glassy-bg-light);
		border: 1px solid var(--glassy-border);
	}
</style>
