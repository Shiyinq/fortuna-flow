<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import DropdownMenu from './DropdownMenu.svelte';

	export let label = '+';
	export let handleClick = (link: string) => {
		goto(link);
		isVisible = false;
		return null;
	};

	const { t } = useTranslation();

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

	$: menuItems = [
		{ label: $t('transactions.addTransaction'), onClick: () => handleClick('/transactions/create') },
		{ label: $t('wallets.newWallet'), onClick: () => handleClick('/wallets/create') },
		{ label: $t('categories.newCategory'), onClick: () => handleClick('/categories/create') }
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
		background: var(--color-bg-2);
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

	:global(.dark) .floating-button {
		background: var(--glassy-bg);
		color: var(--color-theme-1);
	}

	:global(.dark) .floating-button:hover {
		background: var(--color-theme-1);
		color: var(--color-bg-2);
	}

	.floating-button:active {
		transform: translateY(0);
		box-shadow: 0 6px 20px var(--glassy-shadow);
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

	@media (max-width: 1200px) {
		.floating-button-container {
			right: 18vw;
		}
	}

	@media only screen and (max-width: 720px) {
		.floating-button-container {
			right: 20px;
			bottom: 80px;
		}
	}
</style>
