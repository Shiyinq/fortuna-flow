<script lang="ts">
	import SvelteHeatmap from 'svelte-heatmap';

	export let data: any = [];
	export let startDate = '';
	export let endDate = '';
</script>

<div class="container">
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
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
	}
</style>
