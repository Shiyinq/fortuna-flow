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
	import { getChartOptions } from '$lib/utils';

	import EmptyState from '$lib/components/EmptyState.svelte';

	ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

	export let data: any;

	const dataChart = {
		labels: data?.month || [],
		datasets: [
			{
				label: 'Income',
				data: data?.data?.income || [],
				backgroundColor: ['rgba(75, 192, 192, 0.5)']
			},
			{
				label: 'Expense',
				data: data?.data?.expense || [],
				backgroundColor: ['rgba(255, 99, 132, 0.5)']
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
