<script lang="ts">
	import { Pie } from 'svelte-chartjs';
	import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';
	import { darkMode } from '$lib/store';
	import { getChartColors, getComputedStyle } from '$lib/utils';

	import EmptyState from '$lib/components/EmptyState.svelte';

	export let data: any;
	ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

	const pieBgVars = [
		'--chart-pie-1',
		'--chart-pie-2',
		'--chart-pie-3',
		'--chart-pie-4',
		'--chart-pie-5'
	];
	const pieBorderVars = [
		'--chart-pie-1-border',
		'--chart-pie-2-border',
		'--chart-pie-3-border',
		'--chart-pie-4-border',
		'--chart-pie-5-border'
	];
	const pieBgColors = pieBgVars.map((v, i) => getComputedStyle(v, [
		'#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff'][i]
	));
	const pieBorderColors = pieBorderVars.map((v, i) => getComputedStyle(v, [
		'#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff'][i]
	));

	const dataChart = {
		labels: data?.labels || [],
		datasets: [
			{
				data: data?.data || [],
				backgroundColor: pieBgColors,
				borderColor: pieBorderColors,
				borderWidth: 1
			}
		]
	};

	$: colors = getChartColors($darkMode);
	$: options = {
		responsive: true,
		plugins: {
			legend: {
				display: true,
				labels: {
					color: colors.labelColor
				}
			}
		}
	};
</script>

{#if !data?.data?.length}
	<EmptyState />
{:else}
	<div class="chart-container">
		<div class="chart">
			<Pie data={dataChart} {options} />
		</div>
	</div>
{/if}

<style>
	.chart-container {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>
