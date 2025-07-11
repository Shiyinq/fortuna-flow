<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { createCategory } from '$lib/apis/categories';
	import { token } from '$lib/store/index.js';
	import { goto } from '$app/navigation';
	import IconSelector from '$lib/components/IconSelector.svelte';
	import Card from '$lib/components/Card.svelte';
	import { CATEGORY_ICONS } from '$lib/constants';
	import Button from '$lib/components/Button.svelte';

	export let typeForm = 'create';

	let name = '';
	let type: 'expense' | 'income' = 'expense';
	let categoryIcon = '';
	let isFormValid = false;
	let loading = false;

	const createNewCategory = async () => {
		try {
			let response = await createCategory($token, name, type, categoryIcon || undefined);
			toast.success(response.detail);
			name = '';
			type = 'expense';
			categoryIcon = '';
			// Redirect back to categories list
			goto('/categories');
		} catch (error: any) {
			toast.error(error.detail);
		}
	};

	const validateForm = () => {
		isFormValid = name.trim() !== '';
	};

	const handleSave = async () => {
		if (isFormValid) {
			loading = true;
			await createNewCategory();
			loading = false;
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
		<Button variant="primary-solid" fullWidth on:click={handleSave} disabled={!isFormValid} loading={loading}>
			Save Category
		</Button>
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
		border: 1px solid var(--glassy-border);
		border-radius: 5px;
		font-size: 16px;
		background: var(--color-bg-2);
		color: var(--color-text-strong);
		appearance: none;
	}

	input::placeholder,
	select::placeholder {
		color: var(--color-text-muted);
	}

	.form-actions {
		margin-top: 20px;
		display: flex;
		justify-content: center;
	}
</style>
