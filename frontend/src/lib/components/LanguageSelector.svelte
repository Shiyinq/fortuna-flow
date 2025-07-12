<script lang="ts">
	import { currentLanguage } from '$lib/store';
	import { availableLanguages, changeLanguage } from '$lib/i18n';

	// Ambil index bahasa saat ini
	$: langIndex = availableLanguages.findIndex(lang => lang.code === $currentLanguage);
	$: currentLang = availableLanguages[langIndex] || availableLanguages[0];

	function toggleLanguage() {
		const nextIndex = (langIndex + 1) % availableLanguages.length;
		changeLanguage(availableLanguages[nextIndex].code);
	}
</script>

<button class="language-toggle" on:click={toggleLanguage} aria-label="Toggle language">
	<span class="flag">{currentLang.flag}</span>
	<span class="lang-code">{currentLang.code.toUpperCase()}</span>
</button>

<style>
.language-toggle {
	display: flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0.5rem 0.9rem;
	background: var(--background-secondary);
	border: 1px solid var(--border-color);
	border-radius: 0.5rem;
	cursor: pointer;
	transition: all 0.2s ease;
	font-size: 0.95rem;
	color: var(--text-primary);
	font-weight: 600;
}
.language-toggle:hover {
	background: var(--background-hover);
	border-color: var(--border-hover);
}
.flag {
	font-size: 1.25rem;
}
.lang-code {
	font-weight: 600;
	letter-spacing: 1px;
}
</style> 