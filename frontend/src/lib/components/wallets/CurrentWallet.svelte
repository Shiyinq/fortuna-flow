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
		z-index: 100000;
		display: none;
		min-width: 180px;
		margin-top: 12px;
		position: absolute;
		border-radius: 10px;
		background: rgba(255,255,255,0.97);
		box-shadow: 0 4px 24px rgba(44,62,80,0.18);
		border: 1px solid rgba(44,62,80,0.10);
		backdrop-filter: blur(4px);
	}

	.dropdown-content a {
		color: #222;
		display: block;
		padding: 12px 16px;
		text-decoration: none;
		border-radius: 6px;
		transition: background 0.15s;
	}

	.dropdown-content a:hover {
		background: rgba(44,62,80,0.08);
	}

	.show {
		display: block;
	}

	.change-wallet h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.change-wallet h6 {
		font-size: 0.9rem;
		font-weight: 500;
		margin: 0;
		opacity: 0.9;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.current-wallet {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		margin-bottom: 16px;
		overflow: visible;
		position: relative;
	}

	.change-wallet {
		width: 100%;
		display: flex;
		margin-bottom: 4px;
		justify-content: space-between;
	}
</style>
