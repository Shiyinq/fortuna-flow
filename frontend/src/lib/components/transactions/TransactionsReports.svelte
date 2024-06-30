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
	h5 {
		margin-top: 0;
	}

	.analytics-header {
		margin-top: 8px;
	}

	.analytics {
		width: 100%;
		padding: 10px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}
</style>
