<script lang="ts">
	import { onMount } from 'svelte';
	import { formatCurrency } from '$lib/utils';
	import { activeWallet, wallets } from '$lib/store';
	import WalletInfo from '$lib/components/wallets/WalletInfo.svelte';
	import Card from '$lib/components/Card.svelte';
	import DropdownMenu from '../DropdownMenu.svelte';

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

	$: walletMenuItems = $wallets.map((wallet, idxWallet) => ({
		label: wallet?.name,
		onClick: () => selectWallet(wallet, idxWallet)
	}));
</script>

<Card
	className="current-wallet"
	marginBottom={'0px'}
	marginTop={'0px'}
	padding={'0px'}
	showGradient={true}
>
	<div class="change-wallet">
		<h5 class="text-heading">Wallet</h5>
		<!-- svelte-ignore a11y-invalid-attribute -->
		<a href="#" on:click|preventDefault={toggleDropdown}><h6>Change</h6></a>
		<DropdownMenu
			items={walletMenuItems}
			visible={dropdownVisible}
			direction="down"
			marginTop="8px"
		/>
	</div>
	<WalletInfo
		icon={currentWallet?.walletIcon ?? undefined}
		title={currentWallet?.name}
		balance={formatCurrency(currentWallet?.balance ?? 0)}
	/>
</Card>

<style>
	.change-wallet {
		position: relative;
		width: 100%;
		display: flex;
		margin-bottom: 4px;
		justify-content: space-between;
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

	.change-wallet a {
		text-decoration: none;
		color: var(--color-theme-1);
	}

	.change-wallet a:hover {
		opacity: 0.8;
	}
</style>
