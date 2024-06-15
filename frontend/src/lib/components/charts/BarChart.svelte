<script>
	import { Bar } from 'svelte-chartjs';
    import { Chart, registerables } from 'chart.js';

    Chart.register(...registerables);

	let data = {
		labels: ['March', 'April', 'May'],
		datasets: [
			{
				label: 'Total Spent',
				data: [1302401, 4250250, 2500000],
				backgroundColor: [
					'rgba(75, 192, 192, 0.2)',
					'rgba(153, 102, 255, 0.2)',
					'rgba(255, 159, 64, 0.2)'
				],
				borderColor: ['rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'],
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
	<Bar {data} {options} />
</div>

<style>
	.chart-container {
		display: flex;
		justify-content: center;
		align-items: center;
		margin: 20px auto;
	}
</style>
