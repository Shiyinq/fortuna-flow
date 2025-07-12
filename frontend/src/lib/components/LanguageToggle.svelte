<script lang="ts">
import { currentLanguage } from '$lib/store';
import { availableLanguages, changeLanguage } from '$lib/i18n';

$: langIndex = availableLanguages.findIndex(lang => lang.code === $currentLanguage);
$: currentLang = availableLanguages[langIndex] || availableLanguages[0];

function toggleLanguage() {
	const nextIndex = (langIndex + 1) % availableLanguages.length;
	changeLanguage(availableLanguages[nextIndex].code);
}
</script>

<button class="lang-mode-toggle" on:click={toggleLanguage} aria-label="Toggle language">
	<span class="flag">{currentLang.flag}</span>
	<span class="lang-label">{currentLang.name}</span>
</button>

<style>
.lang-mode-toggle {
	display: inline-flex;
	align-items: center;
	gap: 0.5rem;
	padding: 0 1.2rem 0 0.7rem;
	background: rgba(255, 255, 255, 0.2);
	border: 1px solid rgba(255, 255, 255, 0.3);
	border-radius: 12px;
	backdrop-filter: blur(10px);
	-webkit-backdrop-filter: blur(10px);
	color: var(--color-text);
	font-size: 1rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	height: 40px;
}
.lang-mode-toggle:hover {
	background: rgba(255, 255, 255, 0.3);
	transform: translateY(-1px);
	box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}
.lang-mode-toggle:active {
	transform: translateY(0);
}
.flag {
	font-size: 1.25rem;
}
.lang-label {
	font-weight: 700;
	letter-spacing: 1px;
}
</style> 