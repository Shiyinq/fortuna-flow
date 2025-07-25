<script lang="ts">
	import { onMount } from 'svelte';
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
	import DatePicker from '../DatePicker.svelte';
	import Button from '$lib/components/Button.svelte';
	import { toast } from 'svelte-sonner';
	import { useTranslation } from '$lib/i18n/useTranslation';

	AnalyserNode;

	const { t } = useTranslation();

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
			if (transactionId) {
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
				amount = '';
				break;
			case 'backspace': {
				const unformatted = unformatNumber(amount);
				if (unformatted.length > 1) {
					amount = formatNumber(unformatted.slice(0, -1));
				} else {
					amount = '';
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

<Card
	title={transactionId ? $t('transactions.editTransaction') : $t('transactions.addTransaction')}
	showGradient={true}
	className="transaction-form"
	marginTop="0"
	marginBottom="0"
	highlightTitle={true}
>
	{#if transactionId}
		<div class="delete-action">
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" on:click={async () => await deleteData()}>❌ {$t('transactions.deleteTransaction')}</a>
		</div>
	{/if}
	<div class="form-content">
		<AmountInput
		  bind:value={amount}
		  placeholder={$t('transactions.enterAmount')}
		  disabled={false}
		  on:change={(e) => { amount = e.detail; validateForm(); }}
		/>
		<SelectInput bind:value={categoryId} icon="🏷️" label={$t('transactions.category')} placeholder={$t('transactions.selectCategory')} options={categoryOptions} required={true} showManageButton={!transactionId} manageLabel="📁" onManage={() => goto('/categories/create')} on:change={(e) => { categoryId = e.detail; validateForm(); }} />
		<TextInput bind:value={note} icon="📝" placeholder={$t('transactions.enterNote')} maxlength={100} required={false} on:change={(e) => { note = e.detail; }} />
		<div class="form-field">
			<span class="icon">📅</span>
			<DatePicker bind:value={transactionDate} on:change={() => validateForm()} placeholder={$t('transactions.date')}/>
		</div>
		<SelectInput bind:value={walletId} icon="💳" label={$t('transactions.wallet')} placeholder={$t('transactions.selectWallet')} options={paymentMethodOptions} required={true} showManageButton={!transactionId} manageLabel="👛" onManage={() => goto('/wallets/create')} on:change={(e) => { walletId = e.detail; validateForm(); }} disabled={transactionId ? true : false} />
		<Keypad on:keypad={e => handleKeypadInput(e.detail)} />
		<Button variant="primary-solid" fullWidth on:click={handleSubmit} disabled={!isFormValid} loading={loading}>
			{$t('common.save')}
		</Button>
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
		color: var(--color-danger);
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
</style>
