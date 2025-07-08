<script lang="ts">
	import SvelteHeatmap from 'svelte-heatmap';
	import { darkMode } from '$lib/store';
	import { getChartColors } from '$lib/utils';

	export let data: any = [];
	export let startDate = '';
	export let endDate = '';

	$: colors = getChartColors($darkMode);
</script>

<div class="container glassy">
	<SvelteHeatmap
		allowOverflow={true}
		cellGap={5}
		cellRadius={1}
		colors={[
			'var(--chart-heatmap-1, #00C853)',
			'var(--chart-heatmap-2, #33FF99)',
			'var(--chart-heatmap-3, #00E064)',
			'var(--chart-heatmap-4, #009933)'
		]}
		{data}
		dayLabelWidth={20}
		emptyColor={'var(--chart-heatmap-empty, #ecedf0)'}
		{endDate}
		monthGap={20}
		monthLabelHeight={20}
		{startDate}
		view={'monthly'}
		fontColor={colors.fontColor}
	/>
</div>

<style>
	.container {
		margin-bottom: 16px;
		border-radius: 12px;
		padding: 20px;
		width: 100%;
		display: flex;
		flex-direction: column;
	}
</style>
