<script lang="ts">
	import { onMount } from 'svelte';
	import { Toaster, toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';

	import { convertToInteger } from '$lib/utils/index.js';
	import {
		addTransaction,
		deleteTransaction,
		updateTransaction
	} from '$lib/apis/transactions/index.js';
	import { initialTransactionSelected, token, transactionSelected } from '$lib/store/index.js';
	import Card from '$lib/components/Card.svelte';
	import AmountInput from '$lib/components/AmountInput.svelte';
	import TextInput from '$lib/components/TextInput.svelte';
	import SelectInput from '$lib/components/SelectInput.svelte';
	import Keypad from '$lib/components/Keypad.svelte';

	AnalyserNode;

	export let transactionId = $transactionSelected.transactionId;
	export let walletId = $transactionSelected.walletId;
	export let categoryId = $transactionSelected.categoryId;
	export let amount = $transactionSelected.amount.replace(/[^0-9.,]/g, '');
	export let note = $transactionSelected.note;
	export let transactionDate = $transactionSelected.transactionDate;
	export let typeForm = 'edit';

	export let categories: any = [];
	export let paymentMethods: any = [];

	let isFormValid = false;
	let loading = false;

	const validateForm = () => {
		isFormValid =
			amount !== '0' &&
			amount !== '' &&
			categoryId !== '' &&
			transactionDate !== '' &&
			walletId !== '';
	};

	const deleteData = async () => {
		try {
			let response = await deleteTransaction($token, transactionId);
			toast.success(response.detail);
			transactionSelected.set(initialTransactionSelected);
			transactionId = '';
			walletId = '';
			categoryId = '';
			amount = '';
			note = '';
			transactionDate = '';
			typeForm = 'create';
		} catch (error: any) {
			toast.error(error.detail ?? 'Internal Server Error');
		}
	};

	async function handleSubmit() {
		loading = true;
		try {
			const amountInt = parseInt(amount.replace(/\./g, ''));
			if (typeForm === 'edit' && transactionId) {
				await updateTransaction($token, transactionId, categoryId, amountInt, 'expense', note, transactionDate);
				toast.success('Transaction updated successfully!');
			} else {
				await addTransaction($token, walletId, categoryId, amountInt, 'expense', note, transactionDate);
				toast.success('Transaction added successfully!');
			}
			transactionSelected.set(initialTransactionSelected);
			goto('/transactions');
		} catch (e: any) {
			toast.error(e.detail || 'Failed to save transaction');
		} finally {
			loading = false;
		}
	}

	function handleKeypadInput(value: string) {
		const unformatNumber = (num: string) => num.replace(/\./g, '');
		const formatNumber = (num: string) => {
			const parts = num.split(',');
			parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
			return parts.join(',');
		};
		switch (value) {
			case 'C':
				amount = '0';
				break;
			case 'SAVE':
				if (isFormValid) handleSubmit();
				break;
			case 'backspace': {
				const unformatted = unformatNumber(amount);
				if (unformatted.length > 1) {
					amount = formatNumber(unformatted.slice(0, -1));
				} else {
					amount = '0';
				}
				break;
			}
			default:
				amount = formatNumber(unformatNumber(amount) + value);
		}
		validateForm();
	}

	onMount(() => {
		if (typeForm === 'create') {
			transactionSelected.set(initialTransactionSelected);
		}
		validateForm();
	});

	$: categoryOptions = categories.map((cat: any) => ({ value: cat.categoryId, label: cat.name, icon: cat.categoryIcon }));
	$: paymentMethodOptions = paymentMethods.map((method: any) => ({ value: method.walletId, label: method.name, icon: method.walletIcon }));
</script>

<Toaster richColors position="top-center" />
<Card
	title={transactionId ? 'Edit Transaction' : 'Add Transaction'}
	showGradient={true}
	className="transaction-form"
	marginTop="0"
	marginBottom="0"
	highlightTitle={true}
>
	{#if transactionId}
		<div class="delete-action">
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" on:click={async () => await deleteData()}>❌ Delete</a>
		</div>
	{/if}
	<div class="form-content">
		<AmountInput
		  bind:value={amount}
		  placeholder="0"
		  disabled={false}
		  on:change={(e) => { amount = e.detail; validateForm(); }}
		/>
		<SelectInput bind:value={categoryId} icon="🏷️" label="Category" placeholder="Select category" options={categoryOptions} required={true} showManageButton={!transactionId} manageLabel="📁" onManage={() => goto('/transactions/categories')} on:change={(e) => { categoryId = e.detail; validateForm(); }} />
		<TextInput bind:value={note} icon="📝" placeholder="Note" maxlength={100} required={false} on:change={(e) => { note = e.detail; }} />
		<div class="form-field">
			<span class="icon">📅</span>
			<input type="date" bind:value={transactionDate} />
		</div>
		<SelectInput bind:value={walletId} icon="💳" label="Payment Method" placeholder="Select payment method" options={paymentMethodOptions} required={true} showManageButton={!transactionId} manageLabel="👛" onManage={() => goto('/wallets')} on:change={(e) => { walletId = e.detail; validateForm(); }} disabled={transactionId ? true : false} />
		<Keypad on:keypad={e => handleKeypadInput(e.detail)} disabledSave={!isFormValid} />
	</div>
</Card>

<style>
	.delete-action {
		display: flex;
		justify-content: flex-end;
		margin-bottom: 16px;
	}

	.delete-action a {
		text-decoration: none;
		color: #ff4444;
		font-size: 0.9rem;
	}

	.delete-action a:hover {
		opacity: 0.8;
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

	input {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
	}


</style>
