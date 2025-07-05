<script lang="ts">
	import { goto } from '$app/navigation';

	export let label = '+';
	export let handleClick = (link: string) => {
		goto(link);
		return null;
	};

	let isVisible = false;

	const toggleVisibility = () => {
		isVisible = !isVisible;
	};
</script>

<div class="floating-button-container">
	<button class="floating-button" on:click={toggleVisibility}>
		{label}
	</button>

	{#if isVisible}
		<div class="options">
			<button on:click={handleClick('/transactions/create')}>Add Transaction</button>
			<button on:click={handleClick('/wallets/create')}>New Wallet</button>
			<button on:click={handleClick('/transactions/categories/create')}>New Category</button>
		</div>
	{/if}
</div>

<style>
	.floating-button-container {
		position: fixed;
		bottom: 50px;
		right: 20px;
		z-index: 999;
		display: none;
	}

	.floating-button {
		background: rgba(255,255,255,0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		color: var(--color-theme-1);
		border-radius: 50%;
		width: 56px;
		height: 56px;
		cursor: pointer;
		font-size: 24px;
		font-weight: 600;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		transition: all 0.3s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.floating-button:hover {
		background: var(--color-theme-1);
		color: white;
		transform: translateY(-2px);
		box-shadow: 0 12px 40px rgba(0, 200, 83, 0.25);
	}

	.floating-button:active {
		transform: translateY(0);
		box-shadow: 0 6px 20px rgba(0, 200, 83, 0.2);
	}

	.options {
		position: absolute;
		bottom: 70px;
		right: 0;
		background: rgba(255,255,255,0.95);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		border-radius: 12px;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
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
		background: rgba(255,255,255,0.7);
		color: #222;
		border: 1px solid rgba(180,200,220,0.18);
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

	.options button:last-child {
		margin-bottom: 0;
	}

	@media only screen and (max-width: 480px) {
		.floating-button-container {
			display: block;
		}
	}
</style>
