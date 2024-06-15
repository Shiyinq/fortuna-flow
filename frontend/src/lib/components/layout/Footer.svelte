<script>
	import { page } from '$app/stores';
</script>

<footer class="desktop-footer">
    <p>&copy; 2024  <a href="https://github.com/Shiyinq/fortuna-flow">Fortuna Flow</a>. All rights reserved.</p>
</footer>

<footer class="mobile-footer">
	<nav>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,3 L2,0 L2,3 Z" />
		</svg>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
			<li aria-current={$page.url.pathname === '/transactions' ? 'page' : undefined}>
				<a href="/transactions">Transactions</a>
			</li>
			<li aria-current={$page.url.pathname.startsWith('/profile') ? 'page' : undefined}>
				<a href="/profile">Profile</a>
			</li>
		</ul>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L0,3 L2,3 Z" />
		</svg>
	</nav>
</footer>

<style>
    .desktop-footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}

	.desktop-footer a {
		font-weight: bold;
	}

	.mobile-footer {
		width: 100%;
		display: flex;
		position: fixed;
		bottom: 0;
		justify-content: center;
		padding: 0.5em 0;
	}

	nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.7);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-bottom: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}

    .mobile-footer {
        display: none;
    }

    @media only screen and (max-width: 480px) {
		.desktop-footer {
			display: none;
		}
        .mobile-footer {
			padding: 0;
            display: block;
        }
	}
</style>
