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

	const options = {
		responsive: true,
		scales: {
			x: {
				stacked: true
			},
			y: {
				stacked: true
			}
		}
	};
</script>

{#if !data?.data?.income?.length && !data?.data?.expense?.length}
	<EmptyState />
{:else}
	<Bar data={dataChart} {options} />
{/if}
