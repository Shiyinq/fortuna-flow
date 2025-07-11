<script lang="ts">
import { goto } from '$app/navigation';
import { createBudget, updateBudget, deleteBudget } from '$lib/apis/budgets';
import Form from '$lib/components/Form.svelte';
import Button from '$lib/components/Button.svelte';
import { toast } from 'svelte-sonner';
import Card from '$lib/components/Card.svelte';
import { token, currentBudget } from '$lib/store';
import { onMount } from 'svelte';
import AmountInput from '$lib/components/AmountInput.svelte';
import TextInput from '$lib/components/TextInput.svelte';
import SelectInput from '$lib/components/SelectInput.svelte';
import Keypad from '$lib/components/Keypad.svelte';
import DatePicker from '$lib/components/DatePicker.svelte';

export let data;

let name = '';
let amount = '';
let walletId = '';
let categoryId = '';
let type: 'this_month' | 'this_week' | 'custom' = 'this_month';
let startDate = '';
let endDate = '';
let loading = false;
let wallets = data.wallets || [];
let categories = data.categories || [];
let isFormValid = false;
let isEdit = false;
let editBudgetId = '';

const formatNumber = (num: string): string => {
  const parts = num.split(',');
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return parts.join(',');
};

const unformatNumber = (num: string): string => {
  return num.replace(/\./g, '');
};

const updateAmount = (value: string) => {
  const unformattedAmount = unformatNumber(amount);
  if (unformattedAmount === '0' && value !== '000' && value !== ',') {
    amount = formatNumber(value);
  } else {
    amount = formatNumber(unformatNumber(amount) + value);
  }
};

const handleBackspace = () => {
  const unformattedAmount = unformatNumber(amount);
  if (unformattedAmount.length > 1) {
    amount = formatNumber(unformattedAmount.slice(0, -1));
  } else {
    amount = '0';
  }
};

const validateForm = () => {
  isFormValid =
    unformatNumber(amount) !== '0' &&
    name !== '' &&
    walletId !== '' &&
    categoryId !== '';
};

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
  handleInput();
}

const handleKeyboardInput = (event: KeyboardEvent) => {
  if (
    !/^[0-9,]$/.test(event.key) &&
    !['Backspace', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(event.key)
  ) {
    event.preventDefault();
  }
  if (event.key === 'Enter') {
    handleKeypadInput('SAVE');
  }
  if (event.key === 'Backspace') {
    handleBackspace();
  }
};

const handlePaste = (event: ClipboardEvent) => {
  event.preventDefault();
  const pastedText = event.clipboardData?.getData('text');
  if (pastedText) {
    const sanitizedText = pastedText.replace(/[^0-9,]/g, '');
    updateAmount(sanitizedText);
  }
};

const handleInput = () => {
  const unformattedAmount = unformatNumber(amount);
  amount = formatNumber(unformattedAmount);
  validateForm();
};

$: {
  amount;
  name;
  categoryId;
  walletId;
  validateForm();
}

$: walletOptions = wallets.map((w: any) => ({ value: w.walletId, label: w.name, icon: w.walletIcon }));
$: categoryOptions = categories.map((c: any) => ({ value: c.categoryId, label: c.name, icon: c.categoryIcon }));

function resetForm() {
  name = '';
  amount = '0';
  walletId = '';
  categoryId = '';
  type = 'this_month';
  startDate = '';
  endDate = '';
}

async function handleSubmit() {
  loading = true;
  try {
    const dataToSend: any = {
      name,
      amount: parseInt(unformatNumber(amount)),
      walletId,
      categoryId,
      type,
      startDate: type === 'custom' ? startDate : undefined,
      endDate: type === 'custom' ? endDate : undefined
    };
    if (isEdit && editBudgetId) {
      await updateBudget($token, editBudgetId, dataToSend);
      toast.success('Budget updated successfully!');
    } else {
      await createBudget($token, dataToSend);
      toast.success('Budget created successfully!');
    }
    resetForm();
    goto('/budgets');
  } catch (e: any) {
    toast.error(e.detail || (isEdit ? 'Failed to update budget' : 'Failed to create budget'));
  } finally {
    loading = false;
  }
}

async function handleDelete() {
  if (!editBudgetId) return;
  if (confirm('Are you sure you want to delete this budget?')) {
    loading = true;
    try {
      await deleteBudget($token, editBudgetId);
      toast.success('Budget deleted successfully!');
      goto('/budgets');
    } catch (e: any) {
      toast.error(e.detail || 'Failed to delete budget');
    } finally {
      loading = false;
    }
  }
}

onMount(() => {
  validateForm();
  if ($currentBudget) {
    name = $currentBudget.name;
    amount = $currentBudget.amount.toString();
    walletId = $currentBudget.walletId ?? '';
    categoryId = $currentBudget.categoryId ?? '';
    type = $currentBudget.type ?? 'this_month';
    startDate = $currentBudget.startDate;
    endDate = $currentBudget.endDate;
    if ($currentBudget.budgetId) {
      isEdit = true;
      editBudgetId = $currentBudget.budgetId;
    }
    currentBudget.set(null);
  }
});
</script>

<Card title={isEdit ? 'Edit Budget' : 'Add Budget'} showGradient={true} className="budget-form" marginTop="0" marginBottom="0" highlightTitle={true}>
  {#if isEdit}
    <div class="delete-action-budget">
      <button type="button" class="delete-link" on:click={handleDelete}>❌ Delete</button>
    </div>
  {/if}
  <form class="form-content" on:submit|preventDefault={handleSubmit}>
    <AmountInput
      bind:value={amount}
      placeholder="0"
      disabled={loading}
      on:change={(e) => { amount = e.detail; handleInput(); }}
    />
    <TextInput
      bind:value={name}
      icon="📝"
      placeholder="Budget name"
      maxlength={50}
      required={true}
      on:change={(e) => { name = e.detail; validateForm(); }}
    />
    <SelectInput
      bind:value={walletId}
      icon="💳"
      label="Wallet"
      placeholder="Select wallet"
      options={walletOptions}
      required={true}
      showManageButton={true}
      manageLabel="👛"
      onManage={() => goto('/wallets/create')}
      on:change={(e) => { walletId = e.detail; validateForm(); }}
    />
    <SelectInput
      bind:value={categoryId}
      icon="🏷️"
      label="Category"
      placeholder="Select category"
      options={categoryOptions}
      required={true}
      showManageButton={true}
      manageLabel="📁"
      onManage={() => goto('/categories/create')}
      on:change={(e) => { categoryId = e.detail; validateForm(); }}
    />
    <div class="form-field">
      <span class="icon">📅</span>
      <select bind:value={type}>
        <option value="this_month">This Month</option>
        <option value="this_week">This Week</option>
        <option value="custom">Custom</option>
      </select>
    </div>
    {#if type === 'custom'}
      <div class="form-field">
        <span class="icon">📅</span>
        <DatePicker bind:value={startDate} placeholder="Start date" on:change={() => validateForm()} />
      </div>
      <div class="form-field">
        <span class="icon">📅</span>
        <DatePicker bind:value={endDate} placeholder="End date" on:change={() => validateForm()} />
      </div>
    {/if}
    <Keypad on:keypad={e => handleKeypadInput(e.detail)} />
    <Button variant="primary-solid" fullWidth on:click={handleSubmit} disabled={!isFormValid}>
      Save
    </Button>
  </form>
</Card>

<style>
.form-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.form-field {
  display: flex;
  align-items: center;
  gap: 12px;
}
.icon {
  font-size: 20px;
}
select {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--glassy-border);
  border-radius: 5px;
  font-size: 16px;
  background: var(--color-bg-2);
  color: var(--color-text-strong);
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
}
.delete-action-budget {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}
.delete-link {
  background: none;
  border: none;
  color: var(--color-danger);
  font-size: 0.9rem;
  text-decoration: none;
  cursor: pointer;
  padding: 0;
}
.delete-link:hover {
  opacity: 0.8;
}
</style> 