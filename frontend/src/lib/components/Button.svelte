<script lang="ts">
	export let variant: 'primary' | 'secondary' | 'danger' = 'primary';
	export let size: 'small' | 'medium' | 'large' = 'medium';
	export let fullWidth: boolean = false;
	export let disabled: boolean = false;
	export let className: string = '';
	export let type: 'button' | 'submit' = 'button';
</script>

<button 
	class="btn btn-{variant} btn-{size} {fullWidth ? 'btn-full' : ''} {className}"
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
		transition: all 0.15s ease;
		backdrop-filter: blur(6px);
		border: 1.5px solid;
		text-transform: uppercase;
		box-shadow: 0 4px 16px rgba(180, 200, 220, 0.10);
	}

	.btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	/* Variants */
	.btn-primary {
		color: var(--color-theme-1);
		background: rgba(255,255,255,0.7);
		border-color: var(--color-theme-1);
	}

	.btn-primary:hover:not(:disabled) {
		background: var(--color-theme-1);
		color: #fff;
		box-shadow: 0 6px 24px rgba(0,200,83,0.18);
	}

	.btn-secondary {
		color: #222;
		background: rgba(255,255,255,0.7);
		border-color: #d1d5db;
	}

	.btn-secondary:hover:not(:disabled) {
		background: #f0f0f0;
		border-color: var(--color-theme-1);
	}

	.btn-danger {
		color: #ff4c4c;
		background: rgba(255,255,255,0.7);
		border-color: #ff4c4c;
	}

	.btn-danger:hover:not(:disabled) {
		background: #ff4c4c;
		color: #fff;
		box-shadow: 0 6px 24px rgba(255,76,76,0.18);
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