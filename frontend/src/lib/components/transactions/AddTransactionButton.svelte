<script lang="ts">
	import Button from '../Button.svelte';
	import { goto } from '$app/navigation';
	import { useTranslation } from '$lib/i18n/useTranslation';
	const { t } = useTranslation();
</script>

<div class="add-transaction">
	<Button variant="primary-solid" fullWidth on:click={() => goto('/transactions/create')}>
		+ {$t('transactions.addTransaction')}
	</Button>
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
