<script>
    import ollama from 'ollama';
    import { marked } from 'marked';

	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	import { currentTransaction } from '$lib/store';

    marked.setOptions({
		breaks: true
	});

    let loading = true;
    let aiResponse = '';

    const getAiResponse = async () => {
        const prompt = 'Please provide a summary, analysis, and the best advice you can give.\nThis is my transaction data:\n';
        const model =  'llama3:instruct';
        const response = await ollama.chat({
            model: model,
            messages: [{ role: 'user', content: `${prompt} ${JSON.stringify($currentTransaction)}` }],
        })
        return response.message.content;
    }
    
    onMount(async () => {
        if ($currentTransaction.length == 0) {
            goto('/transactions');
        }
        aiResponse = await getAiResponse();
        loading = false;
    });
</script>

<div class="ask-ai">
    {#if loading}
        <div class="loading-response-ai">
            <div class="emoji-ai">
                ✨
            </div>
            <p>Please wait, analyzing your data...</p>
        </div>
    {:else}
        <div class="emoji-ai">
            ✨
        </div>
        <p>{@html marked(aiResponse)}</p>
    {/if}
</div>

<style>
    .loading-response-ai {
        display: flex;
        font-size: 15px;
        text-align: center;
        align-items: center;
        flex-direction: column;
        justify-content: center;
        height: 70vh;
    }

    .emoji-ai {
        font-size: 50px;
    }
</style>