<div class="add-transaction">
	<a href="/transactions/create" class="glassy-button">+ Add Transaction</a>
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
		text-decoration: none;
	}

	.add-transaction a:hover {
		text-decoration: none;
		color: #fff;
	}

	@media only screen and (max-width: 480px) {
		.add-transaction {
			display: none;
		}
	}
</style>
