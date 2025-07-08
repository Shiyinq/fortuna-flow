<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import DropdownMenu from './DropdownMenu.svelte';

	export let label = '+';
	export let handleClick = (link: string) => {
		goto(link);
		isVisible = false;
		return null;
	};

	let isVisible = false;

	const toggleVisibility = () => {
		isVisible = !isVisible;
	};

	// Show floating button only on specific pages
	$: showFloatingButton =
		$page.url.pathname === '/' ||
		$page.url.pathname === '/transactions' ||
		$page.url.pathname === '/wallets';

	// Close menu when clicking outside
	onMount(() => {
		const handleClickOutside = (event: MouseEvent) => {
			const target = event.target as HTMLElement;
			if (!target.closest('.floating-button-container')) {
				isVisible = false;
			}
		};

		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});

	// Close menu when clicking outside
	const handleClickOutside = (event: MouseEvent) => {
		const target = event.target as HTMLElement;
		if (!target.closest('.floating-button-container')) {
			isVisible = false;
		}
	};

	// Close menu when page changes
	$: if ($page.url.pathname) {
		isVisible = false;
	}

	let menuItems = [
		{ label: 'Add Transaction', onClick: () => handleClick('/transactions/create') },
		{ label: 'New Wallet', onClick: () => handleClick('/wallets/create') },
		{ label: 'New Category', onClick: () => handleClick('/categories/create') }
	];
</script>

{#if showFloatingButton}
	<div class="floating-button-container">
		<button
			class="floating-button glassy"
			on:click={(e) => {
				e.stopPropagation();
				toggleVisibility();
			}}
		>
			{label}
		</button>

		<DropdownMenu items={menuItems} visible={isVisible} direction="up" />
	</div>
{/if}

<style>
	.floating-button-container {
		position: fixed;
		bottom: 90px;
		right: 400px;
		z-index: 999;
		display: block;
	}

	.floating-button {
		color: var(--color-theme-1);
		border-radius: 50%;
		width: 56px;
		height: 56px;
		cursor: pointer;
		font-size: 24px;
		font-weight: 600;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	:root.dark .floating-button {
		background: rgba(30, 41, 59, 0.85);
		color: var(--color-theme-1);
		border: 1.5px solid var(--color-theme-1);
	}

	:root.dark .floating-button:hover {
		background: var(--color-theme-1);
		color: #fff;
	}

	.floating-button:active {
		transform: translateY(0);
		box-shadow: 0 6px 20px rgba(0, 200, 83, 0.2);
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@media only screen and (max-width: 480px) {
		.floating-button-container {
			right: 20px;
			bottom: 80px;
		}
	}
</style>
