<script lang="ts">
	import { activeMonth } from '$lib/store';

	const monthNames = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	const currentDate = new Date();

	let currentMonth = currentDate.getMonth();
	let currentYear = currentDate.getFullYear();

	let months = [];
	for (let i = 0; i < 12; i++) {
		let monthIndex = currentMonth - i;
		let year = currentYear;

		if (monthIndex < 0) {
			monthIndex += 12;
			year -= 1;
		}

		months.push({ month: monthNames[monthIndex], monthIndex: monthIndex + 1, year });
	}

	const createMonthYear = (monthIndex: number, year: number) => {
		const formattedMonth = String(monthIndex).padStart(2, '0');
		let monthYear = `${formattedMonth}/${year}`;
		return monthYear;
	};

	const selectMonth = (monthIndex: number, year: number) => {
		activeMonth.set(createMonthYear(monthIndex, year));
	};
</script>

<div class="month-container">
	{#each months as { month, monthIndex, year }}
		<button
			class={$activeMonth == createMonthYear(monthIndex, year) ? 'month selected' : 'month'}
			on:click={() => selectMonth(monthIndex, year)}>{month} {year}</button
		>
	{/each}
</div>

<style>
	.month-container {
		width: 100%;
		display: flex;
		overflow-x: auto;
		white-space: nowrap;
	}

	.month-container .selected {
		border: 1px solid var(--color-theme-1);
	}

	.month {
		padding: 8px;
		margin: 0 10px;
		cursor: pointer;
		font-size: 14px;
		border-radius: 8px;
		border: 1px solid #fff;
		background-color: #fff;
	}

	.month-container::-webkit-scrollbar {
		display: none; /* Safari and Chrome */
	}
</style>
