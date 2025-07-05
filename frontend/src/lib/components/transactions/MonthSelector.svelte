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
		position: static;
		z-index: -100;
	}

	.month-container .selected {
		border: 1.5px solid var(--color-theme-1);
		background: rgba(255,255,255,0.85);
		color: #222;
		font-weight: 600;
	}

	.month {
		padding: 10px 18px;
		margin: 0 8px;
		cursor: pointer;
		font-size: 14px;
		border-radius: 10px;
		border: 1px solid rgba(180,200,220,0.18);
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(6px);
		color: #222;
		transition: background 0.15s, color 0.15s, border 0.15s;
		position: static;
		z-index: auto;
	}

	.month:hover {
		background: rgba(44,62,80,0.08);
	}

	.month-container::-webkit-scrollbar {
		display: none; /* Safari and Chrome */
	}
</style>
