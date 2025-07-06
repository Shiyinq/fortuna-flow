<script lang="ts">
	import { onMount } from 'svelte';
	import { Toaster, toast } from 'svelte-sonner';
	import { createCategory } from '$lib/apis/categories';
	import { token } from '$lib/store/index.js';
	import { goto } from '$app/navigation';

	export let typeForm = 'create';

	let name = '';
	let type: 'expense' | 'income' = 'expense';
	let categoryIcon = '';
	let isFormValid = false;

	const categoryIcons = [
		'🍔', '🚗', '🏠', '💊', '👕', '🎬', '📚', '🎮', '✈️', '🏖️',
		'💼', '🎓', '💻', '📱', '🎵', '🏋️', '🧘', '🎨', '📷', '🌱',
		'💰', '💳', '🏦', '📈', '💎', '🎁', '🎉', '🏆', '⭐', '💡'
	];

	const createNewCategory = async () => {
		try {
			let response = await createCategory($token, name, type, categoryIcon || undefined);
			toast.success(response.detail);
			name = '';
			type = 'expense';
			categoryIcon = '';
			// Redirect back to categories list
			goto('/transactions/categories');
		} catch (error: any) {
			toast.error(error.detail);
		}
	};

	const validateForm = () => {
		isFormValid = name.trim() !== '';
	};

	const handleSave = async () => {
		if (isFormValid) {
			await createNewCategory();
		}
	};

	const handleKeyboardInput = (event: KeyboardEvent) => {
		if (event.key === 'Enter') {
			handleSave();
		}
	};

	const selectIcon = (icon: string) => {
		categoryIcon = categoryIcon === icon ? '' : icon;
	};

	$: {
		name;
		validateForm();
	}

	onMount(() => {
		validateForm();
	});
</script>

<Toaster richColors position="top-center" />

<div class="category-form">
	{#if typeForm == "create"}
		<div class="form-header">
			<h5>Add Category</h5>
		</div>
	{/if}
	<div class="form-content">
		<div class="form-field">
			<span class="icon">📝</span>
			<input 
				type="text" 
				placeholder="Category Name" 
				bind:value={name}
				on:keydown={handleKeyboardInput}
				maxlength="20"
			/>
		</div>

		<div class="form-field">
			<span class="icon">💰</span>
			<select bind:value={type}>
				<option value="expense">Expense</option>
				<option value="income">Income</option>
			</select>
		</div>

		<div class="icon-selection">
			<span class="icon">🎨</span>
			<div class="icon-grid">
				{#each categoryIcons as icon}
					<button
						type="button"
						class="icon-option {categoryIcon === icon ? 'selected' : ''}"
						on:click={() => selectIcon(icon)}
					>
						{icon}
					</button>
				{/each}
			</div>
			{#if categoryIcon}
				<div class="selected-icon">
					Selected: <span class="icon">{categoryIcon}</span>
					<button type="button" class="clear-icon" on:click={() => categoryIcon = ''}>
						Clear
					</button>
				</div>
			{/if}
		</div>
	</div>

	<div class="form-actions">
		<button 
			class="save-button" 
			on:click={handleSave}
			disabled={!isFormValid}
		>
			Save Category
		</button>
	</div>
</div>

<style>
	.category-form {
		font-family: Arial, sans-serif;
		max-width: 400px;
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

	.form-field {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.icon {
		font-size: 20px;
	}

	input, select {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
	}

	.icon-selection {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.icon-grid {
		display: grid;
		grid-template-columns: repeat(10, 1fr);
		gap: 5px;
	}

	.icon-option {
		width: 30px;
		height: 30px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		background: #ffffff;
		cursor: pointer;
		font-size: 14px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: background-color 0.3s;
	}

	.icon-option:hover {
		border-color: var(--color-theme-1);
		background: #f0f0f0;
	}

	.icon-option.selected {
		border-color: var(--color-theme-1);
		background: var(--color-theme-1);
		color: white;
	}

	.selected-icon {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px;
		background: #f0f0f0;
		border-radius: 5px;
		font-size: 12px;
	}

	.clear-icon {
		background: none;
		border: none;
		color: #ff4444;
		cursor: pointer;
		font-size: 11px;
		text-decoration: underline;
	}

	.clear-icon:hover {
		color: #ff4444;
	}

	.form-actions {
		margin-top: 20px;
		display: flex;
		justify-content: center;
	}

	.save-button {
		background-color: var(--color-theme-1);
		color: white;
		border: none;
		padding: 15px 30px;
		font-size: 16px;
		cursor: pointer;
		border-radius: 5px;
		font-weight: 500;
		transition: background-color 0.3s;
	}

	.save-button:hover:not(:disabled) {
		background-color: #45a049;
	}

	.save-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style> 