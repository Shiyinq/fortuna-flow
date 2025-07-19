<script lang="ts">
	import { Bar } from 'svelte-chartjs';
	import {
		Chart as ChartJS,
		CategoryScale,
		LinearScale,
		BarElement,
		Title,
		Tooltip,
		Legend
	} from 'chart.js';
	import { isDarkMode } from '$lib/store';
	import { getChartOptions, getComputedStyle } from '$lib/utils';
	import { useTranslation } from '$lib/i18n/useTranslation';

	import EmptyState from '$lib/components/EmptyState.svelte';

	ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

	export let data: any;

	const { t } = useTranslation();

	const incomeColor = getComputedStyle('--color-success', '#51cf66');
	const expenseColor = getComputedStyle('--color-danger', '#ff4c4c');

	$: dataChart = {
		labels: data?.month || [],
		datasets: [
			{
				label: $t('transactions.income'),
				data: data?.data?.income || [],
				backgroundColor: [incomeColor]
			},
			{
				label: $t('transactions.expense'),
				data: data?.data?.expense || [],
				backgroundColor: [expenseColor]
			}
		]
	};

	$: options = getChartOptions($isDarkMode, {
		scales: {
			x: {
				...getChartOptions($isDarkMode).scales.x,
				stacked: true
			},
			y: {
				...getChartOptions($isDarkMode).scales.y,
				stacked: true
			}
		},
		plugins: {
			legend: {
				display: true
			}
		}
	});
</script>

{#if !data?.data?.income?.length && !data?.data?.expense?.length}
	<EmptyState type="noData" />
{:else}
	<div class="chart-container">
		<Bar data={dataChart} {options} />
	</div>
{/if}

<style>
	.chart-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin: 20px auto;
		width: 100%;
	}
</style>
