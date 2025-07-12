<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import { useTranslation } from '$lib/i18n/useTranslation';

	export let transactions: any;

	let totalInflow = 0;
	let totalOutflow = 0;

	const { t } = useTranslation();

	$: if (transactions) {
		totalInflow = 0;
		totalOutflow = 0;
	}

	$: transactions.forEach((item: any) => {
		totalOutflow += item.totalAmountExpense;
		totalInflow += item.totalAmountIncome;
	});
</script>

<div class="transactions-recap glassy">
	<div class="recap-inflow">
		<h5 class="highlight-title">{$t('transactions.income')}</h5>
		<h5 class="highlight-total">{formatCurrency(totalInflow)}</h5>
	</div>
	<div class="recap-outflow">
		<h5 class="highlight-title">{$t('transactions.expense')}</h5>
		<h5 class="highlight-total">{formatCurrency(totalOutflow)}</h5>
	</div>
	<div class="recap-total">
		<h5 class="highlight-total">{formatCurrency(totalInflow - totalOutflow)}</h5>
	</div>
	<a href="/transactions/reports" class="transaction-report">{$t('transactions.viewReport')}</a>
	<a href="/transactions/ask-ai" class="transaction-report">{$t('transactions.askAI')}</a>
</div>

<style>
	h5 {
		font-size: 1rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px var(--glassy-shadow-light);
	}

	.highlight-title {
		color: var(--color-theme-1);
	}
	.highlight-total {
		color: var(--color-text-muted);
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
		color: var(--color-text-strong);
		position: relative;
		overflow: hidden;
	}

	:global(.dark) .transactions-recap {
		color: var(--color-text-heading);
	}
	:global(.dark) .transactions-recap .highlight-title {
		color: var(--color-theme-1);
	}
	:global(.dark) .transactions-recap .highlight-total {
		color: var(--color-text-muted);
	}

	.transactions-recap::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			45deg,
			rgba(255, 255, 255, 0.1) 0%,
			transparent 50%,
			rgba(255, 255, 255, 0.1) 100%
		);
		pointer-events: none;
		border-radius: 16px;
	}

	.transactions-recap .recap-inflow,
	.transactions-recap .recap-outflow {
		display: flex;
		justify-content: space-between;
		margin-bottom: 6px;
	}

	.transactions-recap .recap-total {
		margin-top: 8px;
		text-align: right;
	}

	.transactions-recap .recap-outflow {
		border-bottom: 1px solid var(--glassy-border);
	}
</style>
