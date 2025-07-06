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
		font-size: 1rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.transaction-report {
		font-size: 12px;
		text-align: center;
		margin-top: 12px;
	}

	.transactions-recap {
		width: 100%;
		display: flex;
		padding: 20px;
		border-radius: 16px;
		flex-direction: column;
		border: 1px solid rgba(255,255,255,0.3);
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		color: #222;
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15), 0 1.5px 4px rgba(44,62,80,0.08);
		position: relative;
		overflow: hidden;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.transactions-recap:hover {
		background: rgba(255,255,255,0.7);
		box-shadow: 0 12px 40px rgba(180, 200, 220, 0.2), 0 2px 8px rgba(44,62,80,0.12);
		transform: translateY(-1px);
	}

	.transactions-recap::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(45deg, rgba(255,255,255,0.12) 0%, transparent 50%, rgba(255,255,255,0.12) 100%);
		pointer-events: none;
		border-radius: 16px;
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
		border-bottom: 1px solid rgba(180,200,220,0.15);
	}
</style>
