<script lang="ts">
	import Card from './Card.svelte';
	
	export let title: string = '';
	export let maxWidth: string = '400px';
	export let className: string = '';
	export let showGradient: boolean = false;
</script>

<Card 
	title={title} 
	showGradient={showGradient}
	className="form {className}"
>
	<slot />
</Card>

<style>
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