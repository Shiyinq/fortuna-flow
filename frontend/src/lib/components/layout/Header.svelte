<script>
	import { page } from '$app/stores';
	import github from '$lib/images/github.svg';
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
</script>

<header>
	<div class="corner left">
		<a href="/" class="app-logo">🍀</a>
	</div>

	<nav class="main-nav">
		<ul>
			<li>
				<a href="/" class="nav-link {$page.url.pathname === '/' ? 'active' : ''}">Home</a>
			</li>
			<li>
				<a
					href="/transactions"
					class="nav-link {$page.url.pathname === '/transactions' ? 'active' : ''}">Transactions</a
				>
			</li>
			<li>
				<a
					href="/budgets"
					class="nav-link {$page.url.pathname.startsWith('/budgets') ? 'active' : ''}">Budgets</a
				>
			</li>
			<li>
				<a
					href="/profile"
					class="nav-link {$page.url.pathname.startsWith('/profile') ? 'active' : ''}">Profile</a
				>
			</li>
		</ul>
	</nav>

	<div class="corner right">
		<div class="right-controls">
			<DarkModeToggle />
		</div>
	</div>
</header>

<style>
	header {
		width: 100%;
		display: flex;
		z-index: 9999;
		position: fixed;
		top: 0;
		left: 0;
		justify-content: space-between;
		align-items: center;
		height: 60px;
		background: transparent;
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
		border-bottom: 1px solid rgba(180, 200, 220, 0.18);
		box-shadow:
			0 8px 32px 0 rgba(44, 62, 80, 0.1),
			0 1.5px 4px 0 rgba(44, 62, 80, 0.08);
		padding: 0 16px;
		border-radius: 0 0 18px 18px;
	}

	/* Dark mode header */
	:global(:root.dark) header {
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow:
			0 8px 32px 0 rgba(0, 0, 0, 0.3),
			0 1.5px 4px 0 rgba(0, 0, 0, 0.2);
	}

	.corner {
		width: 3em;
		height: 3em;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 12px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.corner:hover {
		background: rgba(255, 255, 255, 0.2);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	.right-controls {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
		transition: transform 0.3s ease;
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
	}

	.corner:hover img {
		transform: scale(1.1);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.app-logo {
		font-size: 35px;
		text-decoration: none;
		line-height: 1;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
	}

	.corner:hover .app-logo {
		transform: scale(1.1);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	.main-nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.3);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 16px;
		border: 1px solid rgba(255, 255, 255, 0.2);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}

	/* Dark mode navigation */
	:global(:root.dark) .main-nav {
		--background: rgba(30, 41, 59, 0.6);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	ul {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 0 8px;
		margin: 0;
		list-style: none;
		background: var(--background, rgba(255, 255, 255, 0.3));
		border-radius: 18px;
		box-shadow: 0 2px 8px rgba(44, 62, 80, 0.06);
		gap: 8px;
	}

	ul li {
		display: flex;
	}

	ul li a {
		display: flex;
		align-items: center;
		padding: 7px 16px;
		border-radius: 12px;
		font-size: 0.97rem;
		font-weight: 600;
		text-decoration: none;
		background: transparent;
		line-height: 1.1;
		height: 38px;
	}

	ul li a {
		composes: nav-link;
	}

	ul li[aria-current='page'] a {
		composes: nav-link active;
	}

	@media only screen and (max-width: 720px) {
		header {
			height: 56px;
			background: transparent;
			backdrop-filter: blur(20px);
			-webkit-backdrop-filter: blur(20px);
			border-bottom: 1px solid rgba(255, 255, 255, 0.3);
			box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
			padding: 0 12px 8px 12px;
			border-radius: 0 0 18px 18px;
		}
		.corner {
			width: 48px;
			height: 48px;
		}
		.app-logo {
			font-size: 28px;
		}
		.main-nav {
			display: none !important;
		}
	}

	/* Dark mode mobile styles */
	@media only screen and (max-width: 720px) {
		:global(:root.dark) header {
			border-bottom: 1px solid rgba(255, 255, 255, 0.1);
			box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
		}
	}
</style>
