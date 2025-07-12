<script lang="ts">
	import ollama from 'ollama/browser';
	import { marked } from 'marked';
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { currentTransaction } from '$lib/store';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import Button from '$lib/components/Button.svelte';

	const { t } = useTranslation();

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
			error = $t('ai.errorOccurredRendering');
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
			error = $t('ai.errorOccurredFetching');
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
			error = $t('ai.failedToCopy');
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
			<p class="ai-title text-heading">{$t('ai.aiRecommendation')}</p>
			<p>{error}</p>
			<button class="glassy-button" on:click={async () => await getAiResponse()}
				>{$t('ai.tryAgain')}</button
			>
		</div>
	{:else if initialLoading}
		<div class="loading-response-ai">
			<div class="emoji-ai">✨</div>
			<p class="ai-title text-heading">{$t('ai.aiRecommendation')}</p>
			<p>{$t('ai.pleaseWaitAnalyzing')}</p>
		</div>
	{:else if streaming}
		<div class="emoji-ai">✨</div>
		<p class="ai-title text-heading">{$t('ai.aiRecommendation')}</p>
		<p>{@html renderedResponse}</p>
		<p class="streaming-indicator">{$t('ai.typing')}</p>
	{:else}
		<div class="emoji-ai">✨</div>
		<p class="ai-title text-heading">{$t('ai.aiRecommendation')}</p>
		<p>{@html renderedResponse}</p>
		<div class="button-container">
			<Button fullWidth on:click={copyToClipboard}>
				{copySuccess ? $t('ai.copied') : $t('ai.copyToClipboard')}
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
		color: var(--color-text-muted);
		font-style: italic;
	}

	.error-message {
		color: var(--color-danger);
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
	}

	.ai-title {
		font-size: 1.2rem;
		font-weight: 700;
		margin: 0;
		text-align: center;
		color: var(--color-text-heading);
		text-shadow: 0 1px 2px var(--glassy-shadow-light);
		letter-spacing: normal;
	}
</style>
