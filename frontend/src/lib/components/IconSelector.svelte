<script lang="ts">
	export let selectedIcon = '';
	export let icons: string[] = [];
	export let label = '🎨';

	const selectIcon = (icon: string) => {
		selectedIcon = selectedIcon === icon ? '' : icon;
	};

	const clearIcon = () => {
		selectedIcon = '';
	};
</script>

<div class="icon-selection">
	<span class="icon">{label}</span>
	<div class="icon-grid">
		{#each icons as icon}
			<button
				type="button"
				class="icon-option {selectedIcon === icon ? 'selected' : ''}"
				on:click={() => selectIcon(icon)}
			>
				{icon}
			</button>
		{/each}
	</div>
	{#if selectedIcon}
		<div class="selected-icon">
			Selected: <span class="icon">{selectedIcon}</span>
			<button type="button" class="clear-icon" on:click={clearIcon}>
				Clear
			</button>
		</div>
	{/if}
</div>

<style>
	.icon-selection {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.icon {
		font-size: 20px;
	}

	.icon-grid {
		display: grid;
		grid-template-columns: repeat(10, 1fr);
		gap: 5px;
	}

	.icon-option {
		width: 30px;
		height: 30px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		background: #ffffff;
		cursor: pointer;
		font-size: 14px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: background-color 0.3s;
	}

	.icon-option:hover {
		border-color: var(--color-theme-1);
		background: #f0f0f0;
	}

	.icon-option.selected {
		border-color: var(--color-theme-1);
		background: var(--color-theme-1);
		color: white;
	}

	.selected-icon {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px;
		background: #f0f0f0;
		border-radius: 5px;
		font-size: 12px;
	}

	/* Dark mode icon selector */
	:global(:root.dark) .icon-option {
		border: 1px solid rgba(255, 255, 255, 0.2);
		background: rgba(30, 41, 59, 0.8);
		color: #f1f5f9;
	}

	:global(:root.dark) .icon-option:hover {
		border-color: var(--color-theme-1);
		background: rgba(30, 41, 59, 0.9);
	}

	:global(:root.dark) .selected-icon {
		background: rgba(30, 41, 59, 0.6);
		color: #f1f5f9;
	}

	.clear-icon {
		background: none;
		border: none;
		color: #ff4444;
		cursor: pointer;
		font-size: 11px;
		text-decoration: underline;
	}

	.clear-icon:hover {
		color: #ff4444;
	}

	/* Dark mode clear icon */
	:global(:root.dark) .clear-icon {
		color: #ef4444;
	}

	:global(:root.dark) .clear-icon:hover {
		color: #ef4444;
	}
</style> 