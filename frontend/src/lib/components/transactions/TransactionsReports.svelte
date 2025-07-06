<script lang="ts">
	import { onMount } from 'svelte';

	import PieChart from '$lib/components/charts/PieChart.svelte';
	import StackedBarChart from '$lib/components/charts/StackedBarChart.svelte';
	import Card from '$lib/components/Card.svelte';

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

<Card title="Transactions" showGradient={true} marginTop={"0px"} marginBottom={"0px"}>
	<StackedBarChart data={transactionsData} />
</Card>

<br />

<Card title="Expense" showGradient={true} marginTop={"0px"} marginBottom={"0px"}>
	<PieChart data={expenseData} />
</Card>

<br />

<Card title="Income" showGradient={true} marginTop={"0px"} marginBottom={"0px"}>
	<PieChart data={incomeData} />
</Card>
