<script>
	import { darkMode } from '$lib/store';
	
	function toggleDarkMode() {
		$darkMode = !$darkMode;
	}
</script>

<button 
	class="dark-mode-toggle" 
	on:click={toggleDarkMode}
	aria-label={$darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
	title={$darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
>
	<div class="toggle-icon">
		{#if $darkMode}
			<!-- Sun icon -->
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<circle cx="12" cy="12" r="5"/>
				<line x1="12" y1="1" x2="12" y2="3"/>
				<line x1="12" y1="21" x2="12" y2="23"/>
				<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
				<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
				<line x1="1" y1="12" x2="3" y2="12"/>
				<line x1="21" y1="12" x2="23" y2="12"/>
				<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
				<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
			</svg>
		{:else}
			<!-- Moon icon -->
			<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
			</svg>
		{/if}
	</div>
</button>

<style>
	.dark-mode-toggle {
		width: 40px;
		height: 40px;
		border: none;
		border-radius: 12px;
		background: rgba(255, 255, 255, 0.2);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.3);
		color: var(--color-text);
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.dark-mode-toggle:hover {
		background: rgba(255, 255, 255, 0.3);
		transform: translateY(-1px);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
	}

	.dark-mode-toggle:active {
		transform: translateY(0);
	}

	.toggle-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		transition: transform 0.3s ease;
	}

	.dark-mode-toggle:hover .toggle-icon {
		transform: scale(1.1);
	}

	/* Dark mode styles */
	:global(:root.dark) .dark-mode-toggle {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: #f1f5f9;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	:global(:root.dark) .dark-mode-toggle:hover {
		background: rgba(30, 41, 59, 0.8);
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
	}

	/* Animation for icon transition */
	.toggle-icon svg {
		transition: transform 0.3s ease, opacity 0.3s ease;
	}

	.dark-mode-toggle:hover .toggle-icon svg {
		transform: rotate(15deg);
	}
</style> 