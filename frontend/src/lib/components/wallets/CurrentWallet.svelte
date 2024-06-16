<script lang="ts">
	import { onMount } from 'svelte';
	import wallet from '$lib/images/wallet.svg';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';

	let currentWallet = {
		icon: wallet,
		title: 'ATM',
		balance: '10.200.000'
	};

	let wallets = [
		{ title: 'ATM', icon: wallet, balance: '10.200.000' },
		{ title: 'Cash', icon: wallet, balance: '2.000.200' },
		{ title: 'E-wallet', icon: wallet, balance: '3.560.040' }
	];

	let dropdownVisible = false;

	const toggleDropdown = () => {
		dropdownVisible = !dropdownVisible;
	};

	const selectWallet = (wallet: any) => {
		currentWallet = wallet;
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
				{#each wallets as wallet}
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" on:click|preventDefault={() => selectWallet(wallet)}>{wallet.title}</a>
				{/each}
			</div>
		{/if}
	</div>
	<WalletInfo
		icon={currentWallet.icon}
		title={currentWallet.title}
		balance={currentWallet.balance}
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
