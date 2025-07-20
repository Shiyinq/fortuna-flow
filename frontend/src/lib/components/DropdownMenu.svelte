<script lang="ts">
	export let items: { label: string; onClick?: () => void }[] = [];
	export let onSelect: (item: any) => void = () => {};
	export let visible: boolean = false;
	export let className: string = '';
	export let direction: 'up' | 'down' = 'down';
	export let marginTop: string = '0px';
</script>

{#if visible}
	<!-- svelte-ignore a11y-interactive-supports-focus -->
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<div
		class="dropdown-menu glassy {className} {direction}"
		role="menu"
		style="margin-top: {marginTop};"
		on:click|stopPropagation
	>
		{#each items as item}
			<button
				type="button"
				class="glassy-light button-option"
				on:click={() => {
					item.onClick ? item.onClick() : onSelect(item);
				}}
			>
				{item.label}
			</button>
		{/each}
	</div>
{/if}

<style>
	.dropdown-menu {
		position: absolute;
		right: 0;
		min-width: 180px;
		border-radius: 16px;
		padding: 10px 0;
		z-index: 100;
		animation: slideInDown 0.3s ease;
		background: var(--glassy-bg);
		border: 1.5px solid var(--glassy-border);
		box-shadow:
			0 8px 32px var(--glassy-shadow),
			0 2px 8px var(--glassy-shadow-light);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		color: var(--color-text-strong);
	}

	:root.dark .dropdown-menu button {
		color: var(--color-theme-1);
		background: transparent;
	}

	:root.dark .dropdown-menu button:hover {
		background: var(--color-theme-1);
		color: #fff;
	}

	.dropdown-menu.up {
		bottom: 60px;
		top: auto;
		animation: slideInUp 0.3s ease;
	}
	.dropdown-menu.down {
		top: 100%;
		bottom: auto;
		animation: slideInDown 0.3s ease;
	}
	@keyframes slideInDown {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	@keyframes slideInUp {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	.dropdown-menu button {
		display: block;
		width: 100%;
		margin-bottom: 4px;
		padding: 12px 18px;
		color: var(--color-text-strong);
		border-radius: 10px;
		cursor: pointer;
		font-size: 15px;
		font-weight: 500;
		transition: all 0.2s ease;
		text-align: left;
		background: transparent;
		border: none;
		opacity: 0.97;
	}
	.dropdown-menu button:hover {
		background: var(--color-theme-1);
		color: #fff;
		border-color: var(--color-theme-1);
		transform: translateX(2px);
		opacity: 1;
	}
</style>
