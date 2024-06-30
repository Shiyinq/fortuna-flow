<script lang="ts">
	import { formatCurrency } from '$lib/utils';

	export let transactions: any;

	let totalInflow = 0;
	let totalOutflow = 0;

	$: if (transactions) {
		totalInflow = 0;
		totalOutflow = 0;
	}

	$: transactions.forEach((item: any) => {
		totalOutflow += item.totalAmountExpense;
		totalInflow += item.totalAmountIncome;
	});
</script>

<div class="transactions-recap">
	<div class="recap-inflow">
		<h5>Inflow</h5>
		<h5>{formatCurrency(totalInflow)}</h5>
	</div>
	<div class="recap-outflow">
		<h5>Outflow</h5>
		<h5>{formatCurrency(totalOutflow)}</h5>
	</div>
	<div class="recap-total">
		<h5>{formatCurrency(totalInflow - totalOutflow)}</h5>
	</div>
	<a href="/transactions/reports" class="transaction-report">View report for this period</a>
	<a href="/transactions/ask-ai" class="transaction-report">Ask AI to summarize and advice</a>
</div>

<style>
	h5 {
		margin-top: 0;
		margin-bottom: 0;
	}

	.transaction-report {
		font-size: 12px;
		text-align: center;
		margin-top: 12px;
	}

	.transactions-recap {
		width: 100%;
		display: flex;
		padding: 10px;
		border-radius: 8px;
		flex-direction: column;
		border: 1px solid var(--color-bg-0);
		background-color: #fff;
	}

	.transactions-recap .recap-inflow,
	.transactions-recap .recap-outflow {
		display: flex;
		justify-content: space-between;
	}

	.transactions-recap .recap-total {
		margin-top: 8px;
		text-align: right;
	}

	.transactions-recap .recap-outflow {
		border-bottom: 1px solid var(--color-bg-0);
	}
</style>
