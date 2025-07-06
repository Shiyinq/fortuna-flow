<script lang="ts">
	import SvelteHeatmap from 'svelte-heatmap';
	import { darkMode } from '$lib/store';

	export let data: any = [];
	export let startDate = '';
	export let endDate = '';

	$: fontColor = $darkMode ? '#f1f5f9' : '#333';
</script>

<div class="container glassy">
	<SvelteHeatmap
		allowOverflow={true}
		cellGap={5}
		cellRadius={1}
		colors={['#00C853', '#33FF99', '#00E064', '#009933']}
		{data}
		dayLabelWidth={20}
		emptyColor={'#ecedf0'}
		{endDate}
		monthGap={20}
		monthLabelHeight={20}
		{startDate}
		view={'monthly'}
		fontColor={fontColor}
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
