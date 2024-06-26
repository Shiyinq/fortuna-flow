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
		padding: 8px;
		cursor: pointer;
		color: #fafafa;
		text-align: center;
		border-radius: 4px;
		border: 1px solid var(--color-bg-0);
		background-color: var(--color-theme-1);
	}

	@media only screen and (max-width: 480px) {
		.add-transaction {
			display: none;
		}
	}
</style>