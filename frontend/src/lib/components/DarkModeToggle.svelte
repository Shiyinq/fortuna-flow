<script lang="ts">
	import { darkMode } from '$lib/store';
	import { useTranslation } from '$lib/i18n/useTranslation';
	
	export let showLabel = true;
	const { t } = useTranslation();

	let dropdownVisible = false;

	function toggleDropdown() {
		dropdownVisible = !dropdownVisible;
	}

	function selectMode(isDark: boolean) {
		$darkMode = isDark;
		dropdownVisible = false;
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (!target.closest('.dark-mode-selector')) {
			dropdownVisible = false;
		}
	}

	$: modeOptions = [
		{
			id: 'light',
			name: $t('profile.lightMode'),
			icon: '☀️',
			isDark: false
		},
		{
			id: 'dark',
			name: $t('profile.darkMode'),
			icon: '🌙',
			isDark: true
		}
	];

	$: currentMode = modeOptions.find(mode => mode.isDark === $darkMode) || modeOptions[0];
</script>

<div class="dark-mode-selector">
	<button class="mode-button" on:click={toggleDropdown} aria-label="Select theme mode">
		<span class="mode-icon">{currentMode.icon}</span>
		{#if showLabel}
			<span class="mode-name">{currentMode.name}</span>
		{/if}
		<span class="dropdown-arrow">▼</span>
	</button>

	{#if dropdownVisible}
		<div class="mode-dropdown">
			{#each modeOptions as mode}
				<button
					class="mode-option {mode.isDark === $darkMode ? 'active' : ''}"
					on:click={() => selectMode(mode.isDark)}
				>
					<span class="mode-icon">{mode.icon}</span>
					<span class="mode-name">{mode.name}</span>
					{#if mode.isDark === $darkMode}
						<span class="check">✓</span>
					{/if}
				</button>
			{/each}
		</div>
	{/if}
</div>

<svelte:window on:click={handleClickOutside} />

<style>
	.dark-mode-selector {
		position: relative;
		display: inline-block;
	}

	.mode-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background: rgba(255, 255, 255, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 12px;
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		color: var(--color-text);
		font-size: 0.9rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		min-width: 140px;
	}

	.mode-button:hover {
		background: rgba(255, 255, 255, 0.3);
		transform: translateY(-1px);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
	}

	.dropdown-arrow {
		font-size: 0.8rem;
		margin-left: auto;
		transition: transform 0.2s ease;
	}

	.mode-dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: rgba(255, 255, 255, 0.95);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 12px;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
		z-index: 1000;
		margin-top: 0.5rem;
		overflow: hidden;
	}

	.mode-option {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.75rem 1rem;
		width: 100%;
		background: none;
		border: none;
		cursor: pointer;
		transition: background-color 0.2s ease;
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--color-text);
	}

	.mode-option:hover {
		background: rgba(0, 0, 0, 0.05);
	}

	.mode-option.active {
		background: rgba(var(--color-theme-1-rgb), 0.1);
		color: var(--color-theme-1);
		font-weight: 600;
	}

	.mode-icon {
		font-size: 1.2rem;
	}

	.mode-name {
		flex: 1;
		text-align: left;
	}

	.check {
		color: var(--color-success);
		font-weight: bold;
	}

	/* Dark mode styles */
	:global(.dark) .mode-button {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	:global(.dark) .mode-dropdown {
		background: rgba(30, 41, 59, 0.95);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	:global(.dark) .mode-option:hover {
		background: rgba(255, 255, 255, 0.1);
	}
</style>
