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
		background-color: var(--color-theme-1);
		color: #fff;
		border: none;
		border-radius: 50%;
		width: 50px;
		height: 50px;
		cursor: pointer;
		box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
	}

	.options {
		position: absolute;
		bottom: 60px;
		right: 0;
		background-color: #fff;
		border-radius: 5px;
		box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
		padding: 5px;
	}

	.options button {
		display: block;
		margin-bottom: 5px;
		padding: 5px 10px;
		background-color: var(--color-theme-1);
		color: #fff;
		border: none;
		border-radius: 3px;
		cursor: pointer;
	}

	@media only screen and (max-width: 480px) {
		.floating-button-container {
			display: block;
		}
	}
</style>
