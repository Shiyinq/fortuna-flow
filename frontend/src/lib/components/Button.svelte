<script lang="ts">
	export let variant: 'primary' | 'secondary' | 'danger' | 'primary-solid' = 'primary';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let fullWidth: boolean = false;
	export let disabled: boolean = false;
	export let className: string = '';
	export let type: 'button' | 'submit' = 'button';
</script>

<button
	class="btn btn-{variant} btn-{size} {fullWidth ? 'btn-full' : ''} {variant === 'primary'
		? 'glassy-button'
		: variant === 'danger'
			? 'glassy-danger'
			: variant === 'primary-solid'
				? 'primary-solid-btn'
				: 'glassy-light'} {className}"
	{disabled}
	{type}
	on:click
>
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
		color: #fff;
	}

	.btn-secondary {
		color: #222;
	}

	.btn-secondary:hover:not(:disabled) {
		background: #f0f0f0;
		border-color: var(--color-theme-1);
	}

	.btn-danger {
		color: #ff4c4c;
	}

	.btn-danger:hover:not(:disabled) {
		color: #fff;
	}

	.primary-solid-btn {
		background: var(--color-theme-1, #00e6b8);
		color: #fff;
		border: none;
		border-radius: 24px;
		padding: 12px 32px;
		font-size: 1.1rem;
		font-weight: 600;
		cursor: pointer;
		box-shadow: 0 2px 8px rgba(0,0,0,0.07);
		transition: background 0.2s, color 0.2s;
		text-align: center;
		text-decoration: none;
		text-transform: none;
	}

	:root.dark .primary-solid-btn {
		background: var(--color-theme-1, #00e6b8);
		color: #222;
		border: 1.5px solid #fff;
	}

	:root.dark .primary-solid-btn:hover:not(:disabled) {
		background: #00bfae;
		color: #fff;
	}

	.primary-solid-btn:hover:not(:disabled) {
		background: #00bfae;
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
</style>
