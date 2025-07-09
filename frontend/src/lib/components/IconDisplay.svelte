<script lang="ts">
	import { isEmoji } from '$lib/utils';

	export let icon: string;
	export let alt: string = 'Icon';
	export let size: string = '1.2em';
	export let className: string = '';
</script>

{#if isEmoji(icon)}
	<span class="emoji-icon {className}" style="font-size: {size};" role="img" aria-label={alt}>
		{icon}
	</span>
{:else}
	<img class="img-icon {className}" src={icon} {alt} style="width: {size}; height: {size};" />
{/if}

<style>
	.emoji-icon {
		margin-right: 8px;
		display: inline-block;
		line-height: 1;
	}
</style>
