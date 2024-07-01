<script lang="ts">
	import { Pie } from 'svelte-chartjs';
	import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';

	import EmptyState from '$lib/components/EmptyState.svelte';

	export let data: any;
	ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

	const dataChart = {
		labels: data.labels,
		datasets: [
			{
				data: data.data,
				backgroundColor: [
					'rgba(255, 99, 132, 0.8)',
					'rgba(54, 162, 235, 0.8)',
					'rgba(255, 206, 86, 0.8)',
					'rgba(75, 192, 192, 0.8)',
					'rgba(153, 102, 255, 0.8)'
				],
				borderColor: [
					'rgba(255, 99, 132, 1)',
					'rgba(54, 162, 235, 1)',
					'rgba(255, 206, 86, 1)',
					'rgba(75, 192, 192, 1)',
					'rgba(153, 102, 255, 1)'
				],
				borderWidth: 1
			}
		]
	};

	const options = {
		responsive: true
	};
</script>

{#if data.data.length == 0}
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
