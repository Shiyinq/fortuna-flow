<script lang="ts">
	import { activeMonth } from '$lib/store';
	import { t } from '$lib/i18n';

	const currentDate = new Date();

	let currentMonth = currentDate.getMonth();
	let currentYear = currentDate.getFullYear();

	// Reactive statement untuk nama bulan yang akan diupdate ketika bahasa berubah
	$: monthNames = [
		t('months.january'),
		t('months.february'),
		t('months.march'),
		t('months.april'),
		t('months.may'),
		t('months.june'),
		t('months.july'),
		t('months.august'),
		t('months.september'),
		t('months.october'),
		t('months.november'),
		t('months.december')
	];

	// Reactive statement untuk months array yang akan diupdate ketika monthNames berubah
	$: months = (() => {
		let monthsArray = [];
		for (let i = 0; i < 12; i++) {
			let monthIndex = currentMonth - i;
			let year = currentYear;

			if (monthIndex < 0) {
				monthIndex += 12;
				year -= 1;
			}

			monthsArray.push({ month: monthNames[monthIndex], monthIndex: monthIndex + 1, year });
		}
		return monthsArray;
	})();

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
			class={$activeMonth == createMonthYear(monthIndex, year)
				? 'month selected'
				: 'month'}
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
	}

	.month {
		padding: 8px 18px;
		margin: 0 8px;
		cursor: pointer;
		font-size: 1rem;
		border-radius: 20px;
		color: var(--color-text-muted);
		background: none;
		border: none;
		font-weight: 500;
		transition: background 0.2s, color 0.2s;
		white-space: nowrap;
	}

	.month.selected {
		background: var(--color-theme-1);
		color: var(--color-bg-2);
	}

	/* .month:hover {
		background: rgba(44, 62, 80, 0.08);
	} */

	.month-container::-webkit-scrollbar {
		display: none; /* Safari and Chrome */
	}
</style>
