<script lang="ts">
	import { Bar } from 'svelte-chartjs';
	import { Chart, registerables } from 'chart.js';

	import EmptyState from '$lib/components/EmptyState.svelte';

	Chart.register(...registerables);

	export let data: any;

	interface DataColor {
		[key: string]: {
			backgroundColor: string;
			borderColor: string;
		};
	}

	let selectedColor: {
		backgroundColor: string[];
		borderColor: string[];
	} = {
		backgroundColor: [],
		borderColor: []
	};

	let dataColor: DataColor = {
		January: {
			backgroundColor: "rgba(255, 0, 0, 0.2)",
			borderColor: "rgba(255, 0, 0, 1)"
		},
		February: {
			backgroundColor: "rgba(54, 162, 235, 0.2)",
			borderColor: "rgba(54, 162, 235, 1)"
		},
		March: {
			backgroundColor: "rgba(75, 192, 192, 0.2)",
			borderColor: "rgba(75, 192, 192, 1)"
		},
		April: {
			backgroundColor: "rgba(238, 130, 238, 0.2)",
			borderColor: "rgba(238, 130, 238, 1)"
		},
		May: {
			backgroundColor: "rgba(255, 159, 64, 0.2)",
			borderColor: "rgba(255, 159, 64, 1)"
		},
		June: {
			backgroundColor: "rgba(255, 206, 86, 0.2)",
			borderColor: "rgba(255, 206, 86, 1)"
		},
		July: {
			backgroundColor: "rgba(173, 216, 230, 0.2)",
			borderColor: "rgba(173, 216, 230, 1)"
		},
		August: {
			backgroundColor: "rgba(144, 238, 144, 0.2)",
			borderColor: "rgba(144, 238, 144, 1)"
		},
		September: {
			backgroundColor: "rgba(255, 69, 0, 0.2)",
			borderColor: "rgba(255, 69, 0, 1)"
		},
		October: {
			backgroundColor: "rgba(75, 0, 130, 0.2)",
			borderColor: "rgba(75, 0, 130, 1)"
		},
		November: {
			backgroundColor: "rgba(154, 205, 50, 0.2)",
			borderColor: "rgba(154, 205, 50, 1)"
		},
		December: {
			backgroundColor: "rgba(123, 104, 238, 0.2)",
			borderColor: "rgba(123, 104, 238, 1)"
		}
	};

	$: data.month.forEach((month: any) => {
		if (dataColor.hasOwnProperty(month)) {
			selectedColor.backgroundColor.push(dataColor[month].backgroundColor);
			selectedColor.borderColor.push(dataColor[month].borderColor);
		}
	});

	let dataChart = {
		labels: data.month,
		datasets: [
			{
				label: 'Total Spent',
				data: data.data,
				backgroundColor: selectedColor.backgroundColor,
				borderColor: selectedColor.borderColor,
				borderWidth: 1
			}
		]
	};

	let options = {
		responsive: true,
		scales: {
			y: {
				beginAtZero: true,
				display: false
			}
		},
		plugins: {
			legend: {
				display: false
			}
		}
	};
</script>

<div class="chart-container" style="position: relative; ">
	{#if !data.data.length}
		<EmptyState />
	{:else}
		<Bar data={dataChart} {options} />
	{/if}
</div>

<style>
	.chart-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin: 20px auto;
	}
</style>
