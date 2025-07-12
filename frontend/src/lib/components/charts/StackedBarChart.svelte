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
	import { darkMode } from '$lib/store';
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

	$: options = getChartOptions($darkMode, {
		scales: {
			x: {
				...getChartOptions($darkMode).scales.x,
				stacked: true
			},
			y: {
				...getChartOptions($darkMode).scales.y,
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
	<EmptyState />
{:else}
	<Bar data={dataChart} {options} />
{/if}
