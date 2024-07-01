<script lang="ts">
	import SvelteHeatmap from 'svelte-heatmap';

	export let data:any = []
	export let startDate = '';
	export let endDate = '';

</script>

<div class="container">
	<SvelteHeatmap
		allowOverflow={true}
		cellGap={5}
		cellRadius={1}
		colors={['#00C853', '#33FF99', '#00E064', '#009933']}
		data={data}
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
		margin-top: 16px;
		border-radius: 8px;
		padding: 20px;
		width: 100%;
		display: flex;
		flex-direction: column;
		background-color: #fff;
	}
</style>
