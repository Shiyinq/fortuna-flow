<script lang="ts">
	import MyCategories from '$lib/components/categories/MyCategories.svelte';
	export let data;
</script>

<svelte:head>
	<title>Categories</title>
	<meta name="description" content="Fortuna Flow - Manage Categories" />
</svelte:head>

<MyCategories categories={data.categories?.data} /> 