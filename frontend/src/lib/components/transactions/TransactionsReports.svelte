<script lang="ts">
	import { onMount } from 'svelte';

	import PieChart from '$lib/components/charts/PieChart.svelte';
	import StackedBarChart from '$lib/components/charts/StackedBarChart.svelte';

	type Transaction = {
		totalAmountExpense: number;
		totalAmountIncome: number;
		transactions: any[];
		transactionDate: string;
	};

	type Analytic = {
		month: string[];
		data: {
			income: number[];
			expense: number[];
		};
	};

	export let data: any = [];

	let transactionsData: Analytic = {
		month: [],
		data: {
			income: [],
			expense: []
		}
	};

	let expenseData = { labels: [], data: [] };
	let incomeData = { labels: [], data: [] };

	const groupTransaction = () => {
		data.forEach(({ transactions }: any) => {
			transactions.forEach((transaction: any) => {
				let group: any = transaction.type === 'expense' ? expenseData : incomeData;
				let categoryName: string = transaction.categoryDetail.name;
				let amount: number = transaction.amount;

				const categoryIndex = group.labels.indexOf(categoryName);
				if (categoryIndex === -1) {
					group.labels.push(categoryName);
					group.data.push(amount);
				} else {
					group.data[categoryIndex] += amount;
				}
			});
		});
	};

	const formatingTransaction = () => {
		data.forEach((entry: Transaction) => {
			transactionsData.month.push(entry.transactionDate);
			transactionsData.data.income.push(entry.totalAmountIncome);
			transactionsData.data.expense.push(-entry.totalAmountExpense);
		});
	};

	$: if (data || transactionsData || incomeData || expenseData) {
		formatingTransaction();
		groupTransaction();
	}

	onMount(() => {
		formatingTransaction();
		groupTransaction();
	});
</script>

<div class="analytics">
	<div class="analytics-header">
		<h5>Transactions</h5>
	</div>
	<StackedBarChart data={transactionsData} />
</div>

<br />

<div class="analytics">
	<div class="analytics-header">
		<h5>Expense</h5>
	</div>
	<PieChart data={expenseData} />
</div>

<br />

<div class="analytics">
	<div class="analytics-header">
		<h5>Income</h5>
	</div>
	<PieChart data={incomeData} />
</div>

<style>
	.analytics {
		width: 100%;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
		margin-bottom: 16px;
	}

	.analytics-header {
		margin-top: 8px;
		margin-bottom: 12px;
	}

	h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}
</style>
