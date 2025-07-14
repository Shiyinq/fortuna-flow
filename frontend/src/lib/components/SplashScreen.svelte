<script>
	import { useTranslation } from '$lib/i18n/useTranslation';
	export let show = true;
	const { t } = useTranslation();
</script>

<div class="splash-screen" class:hidden={!show}>
	<h1>🍀 { $t('common.welcome') }</h1>
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
		background: var(--color-bg-1);
		color: var(--color-text);
	}

	.splash-screen h1 {
		font-size: 2rem;
		font-weight: 600;
		text-align: center;
		animation: fadeInUp 1s ease-out;
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.hidden {
		display: none;
	}
</style>
