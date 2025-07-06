<div class="add-transaction">
	<a href="/transactions/create">+ Add Transaction</a>
</div>

<style>
	.add-transaction {
		width: 100%;
		display: flex;
		margin-bottom: 20px;
	}

	.add-transaction a {
		width: 100%;
		padding: 12px 0;
		cursor: pointer;
		color: var(--color-theme-1);
		text-align: center;
		font-weight: 700;
		font-size: 1.1rem;
		border-radius: 10px;
		border: 1.5px solid var(--color-theme-1);
		background: rgba(255,255,255,0.7);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		box-shadow: 0 4px 16px rgba(180, 200, 220, 0.10), 0 1px 4px rgba(44,62,80,0.08);
		transition: background 0.15s, color 0.15s, box-shadow 0.15s;
	}

	.add-transaction a:hover {
		background: var(--color-theme-1);
		color: #fff;
		box-shadow: 0 6px 24px rgba(0,200,83,0.18), 0 2px 8px rgba(44,62,80,0.12);
	}

	@media only screen and (max-width: 480px) {
		.add-transaction {
			display: none;
		}
	}
</style>
