<script lang="ts">
	import { onMount } from 'svelte';
	import { Toaster, toast } from 'svelte-sonner';
	import { createCategory } from '$lib/apis/categories';
	import { token } from '$lib/store/index.js';
	import { goto } from '$app/navigation';
	import IconSelector from '$lib/components/IconSelector.svelte';
	import Card from '$lib/components/Card.svelte';
	import { CATEGORY_ICONS } from '$lib/constants';

	export let typeForm = 'create';

	let name = '';
	let type: 'expense' | 'income' = 'expense';
	let categoryIcon = '';
	let isFormValid = false;

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

	$: {
		name;
		validateForm();
	}

	onMount(() => {
		validateForm();
	});
</script>

<Toaster richColors position="top-center" />

<Card
	title={typeForm === 'create' ? 'Add Category' : ''}
	showGradient={true}
	className="category-form"
	marginTop="0"
	marginBottom="0"
	highlightTitle={true}
>
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

		<IconSelector bind:selectedIcon={categoryIcon} icons={CATEGORY_ICONS} label="🎨" />
	</div>

	<div class="form-actions">
		<button class="save-button" on:click={handleSave} disabled={!isFormValid}>
			Save Category
		</button>
	</div>
</Card>

<style>
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

	input,
	select {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
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
