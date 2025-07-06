<script lang="ts">
	import ollama from 'ollama/browser';
	import { marked } from 'marked';
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { currentTransaction } from '$lib/store';
	import Button from '$lib/components/Button.svelte';

	marked.setOptions({
		breaks: true
	});

	let streaming = true;
	let initialLoading = true;
	let error: string | null = null;

	let aiResponse = '';
	let copySuccess = false;
	let renderedResponse = '';

	let lastRenderTime = 0;
	const RENDER_INTERVAL = 100; // ms

	$: {
		if (aiResponse && Date.now() - lastRenderTime > RENDER_INTERVAL) {
			void renderResponse();
		}
	}

	async function renderResponse() {
		try {
			const markedResponse = await marked(aiResponse);
			renderedResponse = markedResponse;
			lastRenderTime = Date.now();
			await tick();
		} catch (err) {
			console.error('Error rendering response:', err);
			error = 'An error occurred while rendering the response.';
		}
	}

	const getAiResponse = async () => {
		const model = 'qwen2:1.5b';
		const prompt =
			'Please provide a summary, analysis, and the best advice you can give.\nThis is my transaction data:\n';

		try {
			const stream = await ollama.chat({
				model: model,
				messages: [{ role: 'user', content: `${prompt} ${JSON.stringify($currentTransaction)}` }],
				stream: true
			});

			initialLoading = false;
			for await (const chunk of stream) {
				aiResponse += chunk.message.content;
			}
		} catch (err) {
			console.error('Error getting AI response:', err);
			error = 'An error occurred while fetching the AI response.';
		} finally {
			streaming = false;
		}
	};

	const copyToClipboard = async () => {
		try {
			await navigator.clipboard.writeText(aiResponse);
			copySuccess = true;
			setTimeout(() => {
				copySuccess = false;
			}, 2000);
		} catch (err) {
			console.error('Failed to copy: ', err);
			error = 'Failed to copy to clipboard';
		}
	};

	onMount(async () => {
		if ($currentTransaction.length === 0) {
			goto('/transactions');
		}
		await getAiResponse();
	});
</script>

<div class="ask-ai glassy">
	{#if error}
		<div class="error-message">
			<div class="emoji-ai">✨</div>
			<p class="ai-title text-heading">AI Recomendation</p>
			<p>{error}</p>
			<button class="glassy-button" on:click={async () => await getAiResponse()}>✨ Try Again</button>
		</div>
	{:else if initialLoading}
		<div class="loading-response-ai">
			<div class="emoji-ai">✨</div>
			<p class="ai-title text-heading">AI Recomendation</p>
			<p>Please wait, analyzing your data...</p>
		</div>
	{:else if streaming}
		<div class="emoji-ai">✨</div>
		<p class="ai-title text-heading">AI Recomendation</p>
		<p>{@html renderedResponse}</p>
		<p class="streaming-indicator">Typing...</p>
	{:else}
		<div class="emoji-ai">✨</div>
		<p class="ai-title text-heading">AI Recomendation</p>
		<p>{@html renderedResponse}</p>
		<div class="button-container">
			<Button fullWidth on:click={copyToClipboard}>
				{copySuccess ? '✅ Copied!' : '📋 Copy to Clipboard'}
			</Button>
		</div>
	{/if}
</div>

<style>
	.loading-response-ai,
	.error-message {
		height: 70vh;
		display: flex;
		font-size: 15px;
		text-align: center;
		align-items: center;
		flex-direction: column;
		justify-content: center;
	}

	.emoji-ai {
		font-size: 50px;
	}

	.streaming-indicator {
		color: #666;
		font-style: italic;
	}

	.error-message {
		color: red;
		text-align: center;
	}

	.button-container {
		display: flex;
		justify-content: center;
		margin-top: 15px;
	}

	.ask-ai {
		width: 100%;
		max-width: 600px;
		margin: 0 auto;
		padding: 24px 20px;
		border-radius: 16px;
		position: relative;
		overflow: hidden;
		margin-top: 32px;
	}

	.ai-title {
		font-size: 1.2rem;
		font-weight: 700;
		margin: 0;
		text-align: center;
		color: var(--color-text-heading);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
		letter-spacing: normal;
	}
</style>
