<script lang="ts">
	import { currentLanguage } from '$lib/store';
	import { availableLanguages, changeLanguage } from '$lib/i18n';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();

	let dropdownVisible = false;

	function toggleDropdown() {
		dropdownVisible = !dropdownVisible;
	}

	function selectLanguage(code: string) {
		changeLanguage(code);
		dropdownVisible = false;
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (!target.closest('.language-selector')) {
			dropdownVisible = false;
		}
	}

	$: currentLang = availableLanguages.find(lang => lang.code === $currentLanguage) || availableLanguages[0];
</script>

<div class="language-selector">
	<button class="language-button" on:click={toggleDropdown} aria-label="Select language">
		<span class="flag">{currentLang.flag}</span>
		<span class="lang-name">{currentLang.name}</span>
		<span class="dropdown-arrow">▼</span>
	</button>

	{#if dropdownVisible}
		<div class="language-dropdown">
			{#each availableLanguages as language}
				<button
					class="language-option {language.code === $currentLanguage ? 'active' : ''}"
					on:click={() => selectLanguage(language.code)}
				>
					<span class="flag">{language.flag}</span>
					<span class="lang-name">{language.name}</span>
					{#if language.code === $currentLanguage}
						<span class="check">✓</span>
					{/if}
				</button>
			{/each}
		</div>
	{/if}
</div>

<svelte:window on:click={handleClickOutside} />

<style>
	.language-selector {
		position: relative;
		display: inline-block;
	}

	.language-button {
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

	.language-button:hover {
		background: rgba(255, 255, 255, 0.3);
		transform: translateY(-1px);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
	}

	.dropdown-arrow {
		font-size: 0.8rem;
		margin-left: auto;
		transition: transform 0.2s ease;
	}

	.language-dropdown {
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

	.language-option {
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

	.language-option:hover {
		background: rgba(0, 0, 0, 0.05);
	}

	.language-option.active {
		background: rgba(var(--color-theme-1-rgb), 0.1);
		color: var(--color-theme-1);
		font-weight: 600;
	}

	.flag {
		font-size: 1.2rem;
	}

	.lang-name {
		flex: 1;
		text-align: left;
	}

	.check {
		color: var(--color-success);
		font-weight: bold;
	}

	/* Dark mode styles */
	:global(.dark) .language-button {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	:global(.dark) .language-dropdown {
		background: rgba(30, 41, 59, 0.95);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	:global(.dark) .language-option:hover {
		background: rgba(255, 255, 255, 0.1);
	}
</style> 