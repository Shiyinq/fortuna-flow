<script lang="ts">
	import IconDisplay from '$lib/components/IconDisplay.svelte';

	export let sidebarOpen: boolean;
	export let chatHistory: Array<{ id: number; title: string; timestamp: Date }>;
	export let onToggleSidebar: () => void;
	export let onNewChat: () => void;
	export let onSelectChat: (chatId: number) => void;

	function formatDate(date: Date): string {
		return date.toLocaleDateString('id-ID', {
			day: '2-digit',
			month: '2-digit',
			year: '2-digit'
		});
	}
</script>

<div class="sidebar {sidebarOpen ? 'open' : 'closed'}">
	<button class="toggle-btn-absolute" on:click={onToggleSidebar} title={sidebarOpen ? 'Sembunyikan Sidebar' : 'Tampilkan Sidebar'}>
		<IconDisplay icon={sidebarOpen ? '◀' : '▶'} size="1rem" />
	</button>
	
	{#if sidebarOpen}
		<div class="sidebar-content">
			<button class="new-chat-btn" on:click={onNewChat}>
				<IconDisplay icon="💬" size="1rem" />
				<span>New Chat</span>
			</button>
			
			<div class="chat-history">
				<h3>Chats</h3>
				<div class="chat-history-list">
					{#each chatHistory as chat}
						<button class="chat-item nav-link" on:click={() => onSelectChat(chat.id)}>
							<IconDisplay icon="📄" size="1rem" />
							<div class="chat-info">
								<span class="chat-title">{chat.title}</span>
								<span class="chat-time">{formatDate(chat.timestamp)}</span>
							</div>
						</button>
					{/each}
				</div>
			</div>
		</div>
	{:else}
		<!-- Sidebar collapsed content -->
		<div class="sidebar-collapsed">
			<button class="new-chat-btn-collapsed" on:click={onNewChat} title="New Chat">
				<IconDisplay icon="💬" size="1rem" />
			</button>
			
			<div class="chat-history-collapsed">
				{#each chatHistory.slice(0, 3) as chat}
					<button 
						class="chat-item-collapsed nav-link" 
						on:click={() => onSelectChat(chat.id)}
						title="{chat.title}"
					>
						<IconDisplay icon="📄" size="0.8rem" />
					</button>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.sidebar {
		background: transparent;
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
		border-right: 1px solid var(--glassy-border);
		transition: width 0.3s ease;
		display: flex;
		flex-direction: column;
		height: 100%;
		box-shadow: 
			0 8px 32px 0 rgba(44, 62, 80, 0.1),
			0 1.5px 4px 0 rgba(44, 62, 80, 0.08);
		position: relative;
		z-index: 1001;
		overflow: hidden;
	}

	/* Dark mode sidebar */
	:global(:root.dark) .sidebar {
		border-right: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 
			0 8px 32px 0 rgba(0, 0, 0, 0.3),
			0 1.5px 4px 0 rgba(0, 0, 0, 0.2);
	}

	.sidebar.closed {
		width: 60px;
	}

	.sidebar.open {
		width: 280px;
	}

	.toggle-btn-absolute {
		position: absolute;
		top: 25px;
		right: -15px;
		background: var(--color-theme-1);
		border: 2px solid var(--glassy-border);
		color: white;
		cursor: pointer;
		padding: 8px;
		border-radius: 50%;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		align-items: center;
		justify-content: center;
		width: 32px;
		height: 32px;
		z-index: 1003;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
	}

	.toggle-btn-absolute:hover {
		background: var(--color-theme-2);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.2);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.sidebar-content {
		flex: 1;
		padding: 20px 16px 16px 16px;
		overflow-y: auto;
		overflow-x: hidden;
	}

	.new-chat-btn {
		width: 95%;
		background: var(--color-theme-1);
		color: white;
		border: none;
		border-radius: 8px;
		padding: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		cursor: pointer;
		font-size: 0.9rem;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		margin-bottom: 20px;
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
	}

	.new-chat-btn:hover {
		background: var(--color-theme-2);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.2);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.chat-history {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}

	.chat-history h3 {
		margin: 0 0 16px 0;
		font-size: 0.9rem;
		color: var(--color-text-secondary);
		letter-spacing: 0.5px;
		font-weight: 600;
		text-align: left;
		width: 100%;
	}

	.chat-history-list {
		display: flex;
		flex-direction: column;
		gap: 4px;
		width: 100%;
		align-items: flex-start;
	}

	.chat-item {
		display: flex;
		align-items: center;
		gap: 12px;
		padding: 7px 16px;
		border-radius: 12px;
		cursor: pointer;
		transition: all 0.18s;
		border: none;
		background: transparent;
		width: 100%;
		text-align: left;
		font-size: 0.97rem;
		font-weight: 600;
		line-height: 1.1;
		height: 38px;
		color: var(--color-text-secondary);
	}

	.chat-item:hover {
		background: var(--glassy-bg-hover);
		color: var(--color-theme-1);
	}

	.chat-item.active {
		background: rgba(var(--color-theme-1-rgb, 0, 200, 83), 0.1);
		color: var(--color-theme-1);
		box-shadow: 0 1px 4px var(--glassy-shadow-light);
	}

	.chat-info {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.chat-title {
		font-size: 0.9rem;
		color: inherit;
		font-weight: 500;
	}

	.chat-time {
		font-size: 0.75rem;
		color: var(--color-text-muted);
	}

	/* Collapsed sidebar styles */
	.sidebar-collapsed {
		flex: 1;
		padding: 16px 8px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
		overflow: hidden;
	}

	.new-chat-btn-collapsed {
		width: 44px;
		height: 44px;
		background: var(--color-theme-1);
		color: white;
		border: none;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.1);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
		flex-shrink: 0;
		margin-top: 0;
	}

	.new-chat-btn-collapsed:hover {
		background: var(--color-theme-2);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(44, 62, 80, 0.2);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.chat-history-collapsed {
		display: flex;
		flex-direction: column;
		gap: 8px;
		align-items: center;
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
	}

	.chat-item-collapsed {
		width: 44px;
		height: 44px;
		background: transparent;
		border: none;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.18s;
		color: var(--color-text-secondary);
		flex-shrink: 0;
	}

	.chat-item-collapsed:hover {
		background: var(--glassy-bg-hover);
		color: var(--color-theme-1);
		transform: scale(1.05);
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.sidebar.open {
			width: 240px;
		}
		
		.toggle-btn-absolute {
			top: 25px;
			right: -12px;
			width: 28px;
			height: 28px;
			padding: 6px;
		}
	}
</style>
