<script>
	import { currentTransaction } from '$lib/store';
	import TransactionsReports from '$lib/components/transactions/TransactionsReports.svelte';
</script>

<TransactionsReports data={$currentTransaction} />
