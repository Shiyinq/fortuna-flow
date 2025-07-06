<script lang="ts">
	export let title: string = '';
	export let maxWidth: string = '400px';
	export let className: string = '';
</script>

<div class="form {className}" style="max-width: {maxWidth};">
	{#if title}
		<div class="form-header">
			<h5>{title}</h5>
		</div>
	{/if}
	
	<div class="form-content">
		<slot />
	</div>
</div>

<style>
	.form {
		font-family: Arial, sans-serif;
		margin: 0 auto;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
	}

	.form-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0 0 16px 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.form-content {
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	/* Form field styling */
	:global(.form-field) {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	:global(.form-field input),
	:global(.form-field select) {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
	}

	:global(.form-field input:focus),
	:global(.form-field select:focus) {
		outline: none;
		border-color: var(--color-theme-1);
	}

	:global(.form-field select) {
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 10px center;
		padding-right: 30px;
	}

	:global(.form-actions) {
		margin-top: 20px;
		display: flex;
		justify-content: center;
	}
</style> 