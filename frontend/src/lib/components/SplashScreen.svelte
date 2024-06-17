<script>
	export let show = true;
</script>

<div class="splash-screen" class:hidden={!show}>
	<h1>💰 Welcome to Fortuna Flow</h1>
</div>

<style>
	.splash-screen {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 9999;
	}

	.hidden {
		display: none;
	}
</style>
