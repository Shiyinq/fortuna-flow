<script lang="ts">
	import { Pie } from 'svelte-chartjs';
	import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';
	import { isDarkMode } from '$lib/store';
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

	$: colors = getChartColors($isDarkMode);
	$: options = {
		responsive: true,
		plugins: {
			legend: {
				display: true,
				labels: {
					color: colors.labelColor
				}
			},
			tooltip: {
				backgroundColor: $isDarkMode ? 'rgba(30, 41, 59, 0.95)' : 'rgba(255, 255, 255, 0.95)',
				titleColor: colors.labelColor,
				bodyColor: colors.labelColor,
				borderColor: $isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
				borderWidth: 1
			}
		}
	};
</script>

{#if !data?.data?.length}
	<EmptyState type="noData" />
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
