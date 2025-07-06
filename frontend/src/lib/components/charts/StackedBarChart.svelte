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

	$: tickColor = $darkMode ? '#f1f5f9' : '#222';

	$: options = {
		responsive: true,
		scales: {
			x: {
				stacked: true,
				ticks: {
					color: tickColor
				},
				grid: {
					color: $darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'
				}
			},
			y: {
				stacked: true,
				ticks: {
					color: tickColor
				},
				grid: {
					color: $darkMode ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'
				}
			}
		},
		plugins: {
			legend: {
				labels: {
					color: tickColor
				}
			}
		}
	};
</script>

{#if !data?.data?.income?.length && !data?.data?.expense?.length}
	<EmptyState />
{:else}
	<Bar data={dataChart} {options} />
{/if}
