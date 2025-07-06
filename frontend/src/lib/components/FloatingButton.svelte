<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

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
	$: showFloatingButton = $page.url.pathname === '/' || 
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
</script>

{#if showFloatingButton}
	<div class="floating-button-container">
		<button class="floating-button glassy" on:click={(e) => {
			e.stopPropagation();
			toggleVisibility();
		}}>
			{label}
		</button>

		{#if isVisible}
			<!-- svelte-ignore a11y-interactive-supports-focus -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<div class="options glassy" role="menu" on:click|stopPropagation>
				<button type="button" class="glassy-light" on:click={() => handleClick('/transactions/create')}>Add Transaction</button>
				<button type="button" class="glassy-light" on:click={() => handleClick('/wallets/create')}>New Wallet</button>
				<button type="button" class="glassy-light" on:click={() => handleClick('/transactions/categories/create')}>New Category</button>
			</div>
		{/if}
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

	.floating-button:hover {
		background: var(--color-theme-1);
		color: white;
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(0, 200, 83, 0.25), 0 2px 8px rgba(44,62,80,0.12);
	}

	.floating-button:active {
		transform: translateY(0);
		box-shadow: 0 6px 20px rgba(0, 200, 83, 0.2);
	}

	.options {
		position: absolute;
		bottom: 60px;
		right: 0;
		border-radius: 12px;
		padding: 8px;
		min-width: 160px;
		animation: slideIn 0.3s ease;
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

	.options button {
		display: block;
		width: 100%;
		margin-bottom: 4px;
		padding: 10px 12px;
		color: #222;
		border-radius: 8px;
		cursor: pointer;
		font-size: 14px;
		font-weight: 500;
		transition: all 0.2s ease;
		text-align: left;
	}

	.options button:hover {
		background: var(--color-theme-1);
		color: white;
		border-color: var(--color-theme-1);
		transform: translateX(2px);
	}

	:global(:root.dark) .options button {
		color: #f1f5f9;
	}

	.options button:last-child {
		margin-bottom: 0;
	}

	@media only screen and (max-width: 480px) {
		.floating-button-container {
			right: 20px;
			bottom: 80px;
		}
		.options {
			bottom: 70px;
		}
	}
</style>
