<script lang="ts">
	export let variant: 'primary' | 'secondary' | 'danger' = 'primary';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let fullWidth: boolean = false;
	export let disabled: boolean = false;
	export let className: string = '';
	export let type: 'button' | 'submit' = 'button';
</script>

<button 
	class="btn btn-{variant} btn-{size} {fullWidth ? 'btn-full' : ''} {variant === 'primary' ? 'glassy-button' : variant === 'danger' ? 'glassy-danger' : 'glassy-light'} {className}"
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