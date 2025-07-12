<script lang="ts">
	import MyCategories from '$lib/components/categories/MyCategories.svelte';
	import { useTranslation } from '$lib/i18n/useTranslation';
	
	const { t } = useTranslation();
	export let data;
</script>

<svelte:head>
	<title>{$t('categories.title')}</title>
	<meta name="description" content="Fortuna Flow - {$t('categories.title')}" />
</svelte:head>

<MyCategories categories={data.categories?.data} /> 