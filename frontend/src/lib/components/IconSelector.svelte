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
		grid-template-columns: repeat(6, 1fr);
		gap: 5px;
		max-width: 100%;
	}

	.icon-option {
		width: 100%;
		height: 100%;
		aspect-ratio: 1/1;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.6rem;
	}
</style> 