<script lang="ts">
	export let variant: 'primary' | 'secondary' | 'danger' | 'primary-solid' = 'primary';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let fullWidth: boolean = false;
	export let disabled: boolean = false;
	export let className: string = '';
	export let type: 'button' | 'submit' = 'button';
	export let loading: boolean = false;
</script>

<button
	class="btn btn-{variant} btn-{size} {fullWidth ? 'btn-full' : ''} {variant === 'primary'
		? 'glassy-button'
		: variant === 'danger'
			? 'glassy-danger'
			: variant === 'primary-solid'
				? 'primary-solid-btn'
				: 'glassy-light'} {className}"
	disabled={disabled || loading}
	type={type}
	on:click
>
	{#if loading}
		<span class="spinner"></span>
	{/if}
	<slot />
</button>

<style>
	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		border-radius: 10px;
		font-weight: 700;
		cursor: pointer;
		text-transform: uppercase;
	}

	.btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	/* Variants */
	.btn-primary {
		color: var(--color-theme-1);
	}

	.btn-primary:hover:not(:disabled) {
		color: var(--color-bg-2);
	}

	.btn-secondary {
		color: var(--color-text-strong);
	}

	.btn-secondary:hover:not(:disabled) {
		background: var(--color-bg-2);
		border-color: var(--color-theme-1);
	}

	.btn-danger {
		color: var(--color-danger);
	}

	.btn-danger:hover:not(:disabled) {
		color: var(--color-bg-2);
	}

	.primary-solid-btn {
		background: var(--color-theme-1);
		color: var(--color-bg-2);
		border: none;
		border-radius: 24px;
		padding: 12px 32px;
		font-size: 1.1rem;
		font-weight: 600;
		cursor: pointer;
		box-shadow: 0 2px 8px var(--glassy-shadow-light);
		transition: background 0.2s, color 0.2s;
		text-align: center;
		text-decoration: none;
		text-transform: none;
	}

	:root.dark .primary-solid-btn {
		background: var(--color-theme-1);
		color: var(--color-text-strong);
		border: 1.5px solid var(--color-bg-2);
	}

	:root.dark .primary-solid-btn:hover:not(:disabled) {
		background: var(--color-theme-1);
		color: var(--color-bg-2);
	}

	.primary-solid-btn:hover:not(:disabled) {
		background: var(--color-theme-1);
	}

	/* Sizes */
	.btn-small {
		padding: 8px 16px;
		font-size: 0.9rem;
	}

	.btn-medium {
		padding: 12px 24px;
		font-size: 1.1rem;
	}

	.btn-large {
		padding: 16px 32px;
		font-size: 1.2rem;
	}

	/* Full width */
	.btn-full {
		width: 100%;
	}

	.spinner {
		display: inline-block;
		width: 1.2em;
		height: 1.2em;
		border: 2.5px solid rgba(0,0,0,0.15);
		border-top: 2.5px solid var(--color-theme-1);
		border-radius: 50%;
		animation: spin 0.7s linear infinite;
		margin-right: 8px;
		vertical-align: middle;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
