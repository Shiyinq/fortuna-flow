<script lang="ts">
	import TransactionForm from '$lib/components/transactions/TransactionForm.svelte';

	export let data;
</script>

<TransactionForm categories={data.categories} paymentMethods={data.wallets} typeForm="create" />
