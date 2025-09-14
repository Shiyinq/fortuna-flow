<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { marked } from 'marked';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import { 
		Sidebar, 
		ChatMessages, 
		ChatInput 
	} from '$lib/components/ai-chat';

	const { t } = useTranslation();

	marked.setOptions({
		breaks: true
	});

	let messages: Array<{ role: 'user' | 'assistant'; content: string; timestamp: Date }> = [];
	let currentMessage = '';
	let isLoading = false;
	let error: string | null = null;
	let renderedResponse = '';
	let sidebarOpen = true;
	let chatHistory = [
		{ id: 1, title: 'Budget Bulanan', timestamp: new Date() },
		{ id: 2, title: 'Tips Investasi', timestamp: new Date() },
		{ id: 3, title: 'Manajemen Hutang', timestamp: new Date() }
	];

	const GEMINI_API_KEY = '';
	const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';

	const FINANCIAL_SYSTEM_PROMPT = `Anda adalah asisten AI finansial yang ahli dalam memberikan saran dan analisis keuangan. 

PERATURAN PENTING:
1. Hanya jawab pertanyaan yang berkaitan dengan keuangan, investasi, budgeting, dan manajemen keuangan
2. Jika pertanyaan tidak berkaitan dengan keuangan, beri tahu bahwa Anda hanya bisa membantu dengan pertanyaan finansial
3. Berikan saran yang praktis dan dapat diimplementasikan
4. Selalu ingatkan bahwa saran Anda bukan nasihat finansial profesional
5. Gunakan bahasa yang mudah dipahami dan ramah

Bidang keahlian Anda meliputi:
- Perencanaan keuangan pribadi
- Budgeting dan pengelolaan pengeluaran
- Investasi dasar (saham, reksadana, emas, dll)
- Manajemen hutang dan kredit
- Perencanaan pensiun
- Asuransi dan proteksi keuangan
- Analisis laporan keuangan sederhana
- Tips menabung dan menghemat uang
`;

	function scrollToBottom() {
		setTimeout(() => {
			const container = document.querySelector('.chat-messages') as HTMLElement;
			if (container) {
				container.scrollTop = container.scrollHeight;
			}
		}, 100);
	}

	async function sendMessage() {
		if (!currentMessage.trim() || isLoading) return;

		const userMessage = currentMessage.trim();
		currentMessage = '';
		
		messages = [...messages, { role: 'user', content: userMessage, timestamp: new Date() }];
		
		scrollToBottom();
		
		isLoading = true;
		error = null;

		try {
			const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					contents: [
						{
							role: 'user',
							parts: [
								{
									text: `${FINANCIAL_SYSTEM_PROMPT}\n\nPertanyaan user: ${userMessage}`
								}
							]
						}
					],
					generationConfig: {
						temperature: 0.7,
						topK: 40,
						topP: 0.95,
						maxOutputTokens: 2048,
					},
					safetySettings: [
						{
							category: 'HARM_CATEGORY_HARASSMENT',
							threshold: 'BLOCK_MEDIUM_AND_ABOVE'
						},
						{
							category: 'HARM_CATEGORY_HATE_SPEECH',
							threshold: 'BLOCK_MEDIUM_AND_ABOVE'
						},
						{
							category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
							threshold: 'BLOCK_MEDIUM_AND_ABOVE'
						},
						{
							category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
							threshold: 'BLOCK_MEDIUM_AND_ABOVE'
						}
					]
				})
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			
			if (data.candidates && data.candidates[0] && data.candidates[0].content) {
				const aiResponse = data.candidates[0].content.parts[0].text;
				
				const markedResponse = await marked(aiResponse);
				renderedResponse = markedResponse;
				
				messages = [...messages, { role: 'assistant', content: aiResponse, timestamp: new Date() }];
				
				scrollToBottom();
			} else {
				throw new Error('Invalid response format from Gemini API');
			}
		} catch (err) {
			console.error('Error getting AI response:', err);
			error = err instanceof Error ? err.message : 'Terjadi kesalahan saat mendapatkan respons AI';
		} finally {
			isLoading = false;
			await tick();
			
			scrollToBottom();
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}

	function clearChat() {
		messages = [];
		error = null;
		renderedResponse = '';
	}

	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}

	function newChat() {
		clearChat();
		const newChatItem = {
			id: Date.now(),
			title: 'Chat Baru',
			timestamp: new Date()
		};
		chatHistory = [newChatItem, ...chatHistory];
	}

	function selectChat(chatId: number) {
		console.log('Selected chat:', chatId);
	}

	function handleMessageChange(value: string) {
		currentMessage = value;
	}

	onMount(() => {
		messages = [{
			role: 'assistant',
			content: 'Halo! Saya adalah asisten AI finansial Anda. Saya siap membantu dengan pertanyaan seputar keuangan, investasi, budgeting, dan manajemen keuangan. Apa yang ingin Anda tanyakan hari ini?',
			timestamp: new Date()
		}];
	});
</script>

<svelte:head>
	<title>AI Chat Finansial - Fortuna Flow</title>
</svelte:head>

<div class="chat-layout">
	<Sidebar 
		{sidebarOpen}
		{chatHistory}
		onToggleSidebar={toggleSidebar}
		onNewChat={newChat}
		onSelectChat={selectChat}
	/>

	<div class="main-chat">
		<ChatMessages 
			{messages}
			{isLoading}
			{error}
			{renderedResponse}
		/>

		<ChatInput 
			{currentMessage}
			{isLoading}
			onMessageChange={handleMessageChange}
			onSendMessage={sendMessage}
			onKeyPress={handleKeyPress}
		/>
	</div>
</div>

<style>
	.chat-layout {
		display: flex;
		width: 100%;
		height: calc(100vh - 60px);
		background: var(--color-bg-0);
		position: fixed;
		top: 60px;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 1000;
		overflow: hidden;
	}

	.main-chat {
		flex: 1;
		display: flex;
		flex-direction: column;
		background: var(--color-bg-0);
		overflow: hidden;
		position: relative;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.chat-layout {
			flex-direction: column;
		}
	}
</style>
