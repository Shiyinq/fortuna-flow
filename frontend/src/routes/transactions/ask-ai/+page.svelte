<script lang="ts">
	import ollama from 'ollama';
	import { marked } from 'marked';
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { currentTransaction } from '$lib/store';

	marked.setOptions({
		breaks: true
	});

	let streaming = true;
	let initialLoading = true;
	let error: string | null = null;

	let aiResponse = '';
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
		const model = 'llama3:instruct';
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

	onMount(async () => {
		if ($currentTransaction.length === 0) {
			goto('/transactions');
		}
		await getAiResponse();
	});
</script>

<div class="ask-ai">
	{#if error}
		<div class="error-message">
			<p>{error}</p>
			<button on:click={async () => await getAiResponse()}>✨ Try Again</button>
		</div>
	{:else if initialLoading}
		<div class="loading-response-ai">
			<div class="emoji-ai">✨</div>
			<p>Please wait, analyzing your data...</p>
		</div>
	{:else if streaming}
		<div class="emoji-ai">✨</div>
		<p>{@html renderedResponse}</p>
		<p class="streaming-indicator">AI is thinking...</p>
	{:else}
		<div class="emoji-ai">✨</div>
		<p>{@html renderedResponse}</p>
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

	.error-message button {
		cursor: pointer;
		margin-top: 10px;
		padding: 5px 10px;
		border-radius: 4px;
		border: 1px solid #ccc;
		background-color: #f0f0f0;
	}
</style>
