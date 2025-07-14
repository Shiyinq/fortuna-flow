<script lang="ts">
	import LoadingState from '$lib/components/LoadingState.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();
	export let data: any;
</script>

{#if data}
	<MyWallets
		wallets={data.wallets?.data || []}
		title={$t('wallets.myWallets')}
		subtitle={$t('wallets.newWallet')}
		subtitleLink="/wallets/create"
		showGradient={true}
		marginTop={'0px'}
		marginBottom={'0px'}
	/>
{:else}
	<div class="wallets glassy">
		<LoadingState message={$t('common.loading')} />
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
