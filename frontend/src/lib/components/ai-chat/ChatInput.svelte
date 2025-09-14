<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import IconDisplay from '$lib/components/IconDisplay.svelte';

	export let currentMessage: string;
	export let isLoading: boolean;
	export let onMessageChange: (value: string) => void;
	export let onSendMessage: () => void;
	export let onKeyPress: (event: KeyboardEvent) => void;

	function handleInputChange(event: Event) {
		const target = event.target as HTMLInputElement;
		onMessageChange(target.value);
	}
</script>

<div class="chat-input-container">
	<div class="input-wrapper">
		<input
			type="text"
			value={currentMessage}
			on:input={handleInputChange}
			placeholder="Tanyakan seputar keuangan, investasi, atau budgeting..."
			on:keydown={onKeyPress}
			disabled={isLoading}
			class="text-input"
		/>
		<button 
			on:click={onSendMessage} 
			disabled={!currentMessage.trim() || isLoading}
			class="send-button {isLoading ? 'loading' : ''}"
		>
			{#if isLoading}
				⏹️
			{:else}
				⬆️
			{/if}
		</button>
	</div>
	
	<div class="input-disclaimer">
		AI-generated, for reference only
	</div>
</div>

<style>
	.chat-input-container {
		display: flex;
		flex-direction: column;
		justify-content: center; 
		align-items: center;
		gap: 4px;
		margin-bottom: 8px;
	}
	/* .chat-input-container {
		background: transparent;
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
		border-top: 1px solid var(--glassy-border);
		padding: 20px 24px;
		box-shadow: 
			0 8px 32px 0 rgba(44, 62, 80, 0.1),
			0 1.5px 4px 0 rgba(44, 62, 80, 0.08);
	} */

	/* Dark mode input container */
	/* :global(:root.dark) .chat-input-container {
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 
			0 8px 32px 0 rgba(0, 0, 0, 0.3),
			0 1.5px 4px 0 rgba(0, 0, 0, 0.2);
	} */

	.input-wrapper {
		display: flex;
		gap: 12px;
		margin-bottom: 12px;
		background: rgba(255, 255, 255, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 30px;
		padding: 8px;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
		width: 70%;
	}

	/* Dark mode input wrapper */
	:global(:root.dark) .input-wrapper {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.text-input {
		flex: 1;
		background: none;
		border: none;
		color: var(--color-text);
		font-size: 1rem;
		padding: 8px 12px;
		outline: none;
		border-radius: 25px;
	}

	.text-input::placeholder {
		color: var(--color-text-muted);
	}

	.send-button {
		background: var(--color-theme-1);
		color: white;
		border: none;
		border-radius: 50%;
		padding: 12px;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
		width: 44px;
		height: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.send-button.loading {
		background: var(--color-theme-2);
		animation: pulse 1.5s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% {
			transform: scale(1);
			opacity: 1;
		}
		50% {
			transform: scale(1.05);
			opacity: 0.8;
		}
	}

	.send-button:hover:not(:disabled) {
		background: var(--color-theme-2);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.2);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.send-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.input-disclaimer {
		text-align: center;
		font-size: 0.8rem;
		color: var(--color-text-muted);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.chat-input-container {
			padding: 16px;
		}
	}
</style>
