<script>
	import { page } from '$app/stores';
	import { useTranslation } from '$lib/i18n/useTranslation';

	const { t } = useTranslation();
</script>

<footer class="desktop-footer">
	<p>
		{$t('footer.copyright')} <a href="https://github.com/Shiyinq/fortuna-flow">Fortuna Flow</a>.
	</p>
</footer>

<footer class="mobile-footer">
	<nav>
		<ul>
			<li>
				<a href="/" class="nav-link {$page.url.pathname === '/' ? 'active' : ''}">
					<svg
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
						<polyline points="9,22 9,12 15,12 15,22" />
					</svg>
					<span>{$t('footer.home')}</span>
				</a>
			</li>
			<li>
				<a
					href="/transactions"
					class="nav-link {$page.url.pathname === '/transactions' ? 'active' : ''}"
				>
					<svg
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
						<polyline points="14,2 14,8 20,8" />
						<line x1="16" y1="13" x2="8" y2="13" />
						<line x1="16" y1="17" x2="8" y2="17" />
						<polyline points="10,9 9,9 8,9" />
					</svg>
					<span>{$t('footer.activity')}</span>
				</a>
			</li>
			<li>
				<a
					href="/budgets"
					class="nav-link {$page.url.pathname.startsWith('/budgets') ? 'active' : ''}"
				>
					<svg
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						class="budget-icon"
					>
						<rect x="3" y="6" width="18" height="13" rx="2"/>
						<path d="M16 3v3"/>
						<path d="M8 3v3"/>
						<path d="M3 10h18"/>
					</svg>
					<span>{$t('footer.budgets')}</span>
				</a>
			</li>
			<li>
				<a
					href="/profile"
					class="nav-link {$page.url.pathname.startsWith('/profile') ? 'active' : ''}"
				>
					<svg
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
						<circle cx="12" cy="7" r="4" />
					</svg>
					<span>{$t('footer.profile')}</span>
				</a>
			</li>
		</ul>
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
		position: fixed;
		bottom: 0;
		left: 0;
		border-radius: 18px 18px 0 0;
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-top: 1px solid var(--glassy-border);
		box-shadow: 0 -4px 20px var(--glassy-shadow);
		z-index: 100;
		padding: 4px 0 0 0;
		margin: 0 auto;
	}

	/* Dark mode footer */
	:global(:root.dark) .mobile-footer {
		border-top: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.3);
	}

	nav {
		width: 100%;
	}

	ul {
		display: flex;
		justify-content: space-around;
		align-items: center;
		list-style: none;
		margin: 0;
		padding: 0 8px;
	}

	li {
		flex: 1;
		display: flex;
		justify-content: center;
	}

	li a {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 6px 4px;
		text-decoration: none;
		border-radius: 14px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		min-height: 44px;
		width: 100%;
		max-width: 72px;
		position: relative;
		overflow: hidden;
	}

	li a {
		composes: nav-link;
	}

	li a::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 16px;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	li a:hover::before {
		opacity: 1;
	}

	li a:hover {
		transform: translateY(-2px);
	}

	li a svg {
		margin-bottom: 2px;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08));
	}

	li a:hover svg {
		transform: scale(1.15);
		filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
	}

	li a span {
		font-size: 0.7rem;
		font-weight: 600;
		text-align: center;
		letter-spacing: 0.5px;
		transition: all 0.3s ease;
		line-height: 1.1;
		padding: 0 2px;
		z-index: 2;
		max-width: 100%;
		word-break: break-word;
		text-overflow: ellipsis;
		overflow: hidden;
		display: block;
		white-space: nowrap;
	}

	li a:hover span {
		transform: scale(1.05);
	}

	/* Hide desktop footer on mobile */
	.mobile-footer {
		display: none;
	}

	@media only screen and (max-width: 720px) {
		.desktop-footer {
			display: none;
		}
		.mobile-footer {
			display: block;
			padding-bottom: calc(4px + env(safe-area-inset-bottom));
		}
	}

	.budget-icon {
		transform: scale(1.18);
	}
</style>
