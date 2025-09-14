<script lang="ts">
	import IconDisplay from '$lib/components/IconDisplay.svelte';

	export let messages: Array<{ role: 'user' | 'assistant'; content: string; timestamp: Date }>;
	export let isLoading: boolean;
	export let error: string | null;
	export let renderedResponse: string;

	function formatTime(date: Date): string {
		return date.toLocaleTimeString('id-ID', { 
			hour: '2-digit', 
			minute: '2-digit' 
		});
	}
</script>

<div class="chat-messages">
	{#each messages as message, index}
		<div class="message {message.role}" class:user-message={message.role === 'user'} class:ai-message={message.role === 'assistant'}>
			<div class="message-avatar">
				{#if message.role === 'user'}
					<!-- User message tanpa icon -->
				{:else}
					<IconDisplay icon="🍀" size="1.5rem" />
				{/if}
			</div>
			<div class="message-content">
				{#if message.role === 'assistant' && index === messages.length - 1 && renderedResponse}
					<div class="ai-response" contenteditable="false" bind:innerHTML={renderedResponse}></div>
				{:else}
					<div class="message-text">{message.content}</div>
				{/if}
				<div class="message-actions">
					{#if message.role === 'user'}
						<button class="action-btn">
							<IconDisplay icon="👁️" size="0.8rem" />
						</button>
						<button class="action-btn">
							<IconDisplay icon="✏️" size="0.8rem" />
						</button>
					{:else}
						<button class="action-btn">
							<IconDisplay icon="🔄" size="0.8rem" />
						</button>
						<button class="action-btn">
							<IconDisplay icon="👍" size="0.8rem" />
						</button>
						<button class="action-btn">
							<IconDisplay icon="👎" size="0.8rem" />
						</button>
						<button class="action-btn">
							<IconDisplay icon="📋" size="0.8rem" />
						</button>
					{/if}
				</div>
			</div>
		</div>
	{/each}

	{#if isLoading}
		<div class="message ai-message">
			<div class="message-avatar">
				<IconDisplay icon="🍀" size="1.5rem" />
			</div>
			<div class="message-content">
				<div class="typing-indicator">
					<span></span>
					<span></span>
					<span></span>
				</div>
			</div>
		</div>
	{/if}

	{#if error}
		<div class="error-message">
			<IconDisplay icon="⚠️" size="1rem" />
			<span>{error}</span>
		</div>
	{/if}
</div>

<style>
	.chat-messages {
		flex: 1;
		overflow-y: auto;
		padding: 24px;
		display: flex;
		flex-direction: column;
		gap: 24px;
		background: transparent;
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
	}

	/* Dark mode chat messages */
	:global(:root.dark) .chat-messages {
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
	}

	.message {
		display: flex;
		gap: 16px;
		align-items: flex-start;
		max-width: 100%;
	}

	.user-message {
		flex-direction: row-reverse;
		justify-content: flex-start;
	}

	.message-avatar {
		flex-shrink: 0;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.user-message .message-avatar {
		width: 0;
		height: 0;
		opacity: 0;
	}

	.message-content {
		flex: 1;
		min-width: 0;
		position: relative;
	}

	.user-message .message-content {
		flex: none;
		width: auto;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
	}

	.message-text {
		background: rgba(255, 255, 255, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		padding: 12px 16px;
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: var(--color-text);
		line-height: 1.6;
		word-wrap: break-word;
		max-width: 80%;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
	}

	/* Dark mode message text */
	:global(:root.dark) .message-text {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.user-message .message-text {
		background: var(--color-theme-1);
		color: white;
		border-color: var(--color-theme-1);
		margin-left: auto;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.2);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
		max-width: fit-content;
		width: auto;
	}

	.ai-message .message-text {
		background: rgba(255, 255, 255, 0.3);
		border-color: rgba(255, 255, 255, 0.2);
		max-width: 80%;
	}

	/* Dark mode AI message text */
	:global(:root.dark) .ai-message .message-text {
		background: rgba(30, 41, 59, 0.6);
		border-color: rgba(255, 255, 255, 0.1);
	}

	.message-actions {
		display: flex;
		gap: 8px;
		margin-top: 8px;
		opacity: 0;
		transition: opacity 0.2s;
	}

	.user-message .message-actions {
		justify-content: flex-end;
	}

	.message:hover .message-actions {
		opacity: 1;
	}

	.action-btn {
		background: none;
		border: none;
		color: var(--color-text-muted);
		cursor: pointer;
		padding: 4px;
		border-radius: 4px;
		transition: all 0.2s;
	}

	.action-btn:hover {
		background: var(--glassy-bg-hover);
		color: var(--color-text);
	}

	.ai-response {
		background: rgba(255, 255, 255, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		padding: 12px 16px;
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: var(--color-text);
		line-height: 1.6;
		max-width: 80%;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
	}

	/* Dark mode AI response */
	:global(:root.dark) .ai-response {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.ai-response :global(h1),
	.ai-response :global(h2),
	.ai-response :global(h3),
	.ai-response :global(h4),
	.ai-response :global(h5),
	.ai-response :global(h6) {
		color: var(--color-text-heading);
		margin: 16px 0 8px 0;
	}

	.ai-response :global(p) {
		margin: 8px 0;
	}

	.ai-response :global(ul),
	.ai-response :global(ol) {
		margin: 8px 0;
		padding-left: 20px;
	}

	.ai-response :global(li) {
		margin: 4px 0;
	}

	.ai-response :global(strong) {
		color: var(--color-text-heading);
		font-weight: 600;
	}

	.ai-response :global(code) {
		background: rgba(255, 255, 255, 0.3);
		padding: 2px 6px;
		border-radius: 4px;
		font-family: var(--font-mono);
		font-size: 0.9em;
	}

	/* Dark mode code */
	:global(:root.dark) .ai-response :global(code) {
		background: rgba(30, 41, 59, 0.6);
	}

	.ai-response :global(blockquote) {
		border-left: 4px solid var(--color-theme-1);
		padding-left: 16px;
		margin: 16px 0;
		font-style: italic;
		color: var(--color-text-secondary);
	}

	.typing-indicator {
		display: flex;
		gap: 4px;
		padding: 12px 16px;
		background: rgba(255, 255, 255, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 12px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		width: fit-content;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
	}

	/* Dark mode typing indicator */
	:global(:root.dark) .typing-indicator {
		background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.typing-indicator span {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--color-theme-1);
		animation: typing 1.4s infinite ease-in-out;
	}

	.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
	.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

	@keyframes typing {
		0%, 80%, 100% {
			transform: scale(0.8);
			opacity: 0.5;
		}
		40% {
			transform: scale(1);
			opacity: 1;
		}
	}

	.error-message {
		background: rgba(255, 76, 76, 0.1);
		border: 1px solid var(--color-danger);
		border-radius: 8px;
		padding: 12px;
		color: var(--color-danger);
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 0.9rem;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.chat-messages {
			padding: 16px;
		}
	}
</style>
