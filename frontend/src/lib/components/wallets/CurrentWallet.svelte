<script lang="ts">
	import { onMount } from 'svelte';
	import { formatCurrency } from '$lib/utils';
	import { activeWallet, wallets } from '$lib/store';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';

	$: currentWallet = $wallets[$activeWallet];

	let dropdownVisible = false;

	const toggleDropdown = () => {
		dropdownVisible = !dropdownVisible;
	};

	const selectWallet = (wallet: any, index: number) => {
		currentWallet = wallet;
		activeWallet.set(index);
		dropdownVisible = false;
	};

	const handleClickOutside = (event: any) => {
		if (!event.target.closest('.current-wallet')) {
			dropdownVisible = false;
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => document.removeEventListener('click', handleClickOutside);
	});
</script>

<div class="current-wallet">
	<div class="change-wallet">
		<h5>Wallet</h5>
		<!-- svelte-ignore a11y-invalid-attribute -->
		<a href="#" on:click|preventDefault={toggleDropdown}><h6>Change</h6></a>
		{#if dropdownVisible}
			<div class="dropdown-content show">
				{#each $wallets as wallet, idxWallet}
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" on:click|preventDefault={() => selectWallet(wallet, idxWallet)}
						>{wallet?.name}</a
					>
				{/each}
			</div>
		{/if}
	</div>
	<WalletInfo
		icon={currentWallet?.walletIcon ?? undefined}
		title={currentWallet?.name}
		balance={formatCurrency(currentWallet?.balance ?? 0)}
	/>
</div>

<style>
	.change-wallet {
		position: relative;
	}

	.dropdown-content {
		right: 0;
		z-index: 1;
		display: none;
		min-width: 160px;
		margin-top: 20px;
		position: absolute;
		border-radius: 8px;
		background-color: #f9f9f9;
		box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
	}

	.dropdown-content a {
		color: black;
		display: block;
		padding: 12px 16px;
		text-decoration: none;
	}

	.dropdown-content a:hover {
		background-color: #f1f1f1;
	}

	.show {
		display: block;
	}

	h5,
	h6 {
		margin-top: 0;
		margin-bottom: 0;
	}

	.current-wallet {
		width: 100%;
	}

	.change-wallet {
		width: 100%;
		display: flex;
		margin-bottom: 4px;
		justify-content: space-between;
	}
</style>
