<script lang="ts">
	import Button from '../Button.svelte';
	import { goto } from '$app/navigation';
</script>

<div class="add-transaction">
	<Button fullWidth on:click={() => goto('/transactions/create')}>+ Add Transaction</Button>
</div>

<style>
	.add-transaction {
		width: 100%;
		display: flex;
		margin-bottom: 20px;
	}

	@media only screen and (max-width: 480px) {
		.add-transaction {
			display: none;
		}
	}
</style>
