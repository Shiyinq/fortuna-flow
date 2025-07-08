<script lang="ts">
import { goto } from '$app/navigation';
import { createBudget } from '$lib/apis/budgets';
import Form from '$lib/components/Form.svelte';
import Button from '$lib/components/Button.svelte';
import { toast } from 'svelte-sonner';
import Card from '$lib/components/Card.svelte';
import { token } from '$lib/store';
import { onMount } from 'svelte';

export let data;

let name = '';
let amount = '0';
let walletId = '';
let categoryId = '';
let type: 'month' | 'this_week' | 'custom' = 'month';
let startDate = '';
let endDate = '';
let loading = false;
let wallets = data.wallets || [];
let categories = data.categories || [];
let isFormValid = false;
let amountInput: HTMLInputElement;

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

const handleKeypadInput = async (value: string) => {
  switch (value) {
    case 'C':
      amount = '0';
      break;
    case 'SAVE':
      if (isFormValid) {
        await handleSubmit();
      }
      break;
    case 'backspace':
      handleBackspace();
      break;
    default:
      updateAmount(value);
  }
  validateForm();
};

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

function resetForm() {
  name = '';
  amount = '0';
  walletId = '';
  categoryId = '';
  type = 'month';
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
    await createBudget($token, dataToSend);
    toast.success('Budget created successfully!');
    resetForm();
    goto('/budgets');
  } catch (e: any) {
    toast.error(e.detail || 'Failed to create budget');
  } finally {
    loading = false;
  }
}

onMount(() => {
  if (amountInput) {
    amountInput.addEventListener('focus', () => {
      if (
        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      ) {
        amountInput.blur();
      }
    });
  }
  validateForm();
});
</script>

<Card title="Add Budget" showGradient={true} className="budget-form">
  <form class="form-content" on:submit|preventDefault={handleSubmit}>
    <div class="amount-input">
      <span class="currency">IDR</span>
      <input 
        type="text" 
        bind:value={amount} 
        placeholder="0" 
        required 
        on:input={handleInput} 
        on:paste={handlePaste} 
        on:keydown={handleKeyboardInput} 
        bind:this={amountInput} 
      />
    </div>
    <div class="form-field">
      <span class="icon">📝</span>
      <input type="text" bind:value={name} maxlength="50" placeholder="Budget name" required />
    </div>
    <div class="form-field">
      <span class="icon">💳</span>
      <select bind:value={walletId} required>
        <option value="" disabled>Select wallet</option>
        {#each wallets as w}
          <option value={w.walletId}>{w.walletIcon ?? '💳'} {w.name}</option>
        {/each}
      </select>
      <button class="manage-wallets-button" on:click={() => goto('/wallets/create')}>
        👛
      </button>
    </div>
    <div class="form-field">
      <span class="icon">🏷️</span>
      <select bind:value={categoryId} required>
        <option value="" disabled>Select category</option>
        {#each categories as c}
          <option value={c.categoryId}>{c.categoryIcon ?? '💰'} {c.name}</option>
        {/each}
      </select>
      <button class="manage-categories-button" on:click={() => goto('/transactions/categories/create')}>
        📁
      </button>
    </div>
    <div class="form-field">
      <span class="icon">📅</span>
      <select bind:value={type}>
        <option value="month">Monthly</option>
        <option value="this_week">This Week</option>
        <option value="custom">Custom</option>
      </select>
    </div>
    {#if type === 'custom'}
      <div class="form-field">
        <span class="icon">📅</span>
        <input type="date" bind:value={startDate} placeholder="Start date" required={type==='custom'} />
      </div>
      <div class="form-field">
        <span class="icon">📅</span>
        <input type="date" bind:value={endDate} placeholder="End date" required={type==='custom'} />
      </div>
    {/if}
  </form>
  <div class="keypad">
    {#each ['7', '8', '9', 'backspace', '4', '5', '6', 'C', '1', '2', '3', 'SAVE', '0', '000', ','] as key}
      <button
        class="keypad-button"
        class:done={key === 'SAVE'}
        class:backspace={key === 'backspace'}
        on:click={async () => await handleKeypadInput(key)}
        disabled={key === 'SAVE' && !isFormValid}
      >
        <span class="button-content">
          {#if key === 'backspace'}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path>
              <line x1="18" y1="9" x2="12" y2="15"></line>
              <line x1="12" y1="9" x2="18" y2="15"></line>
            </svg>
          {:else}
            {key}
          {/if}
        </span>
      </button>
    {/each}
  </div>
</Card>

<style>
.budget-form {
  max-width: 420px;
  margin: 32px auto;
}
.form-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.amount-input {
  display: flex;
  align-items: center;
  font-size: 24px;
  margin-bottom: 20px;
}
.currency {
  background-color: #e0e0e0;
  padding: 5px 10px;
  border-radius: 5px;
  margin-right: 10px;
}
.form-field {
  display: flex;
  align-items: center;
  gap: 12px;
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
  background: #fff;
}
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
}
.form-actions {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
.manage-wallets-button, .manage-categories-button {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  min-width: 40px;
  height: 40px;
}

.manage-wallets-button:hover, .manage-categories-button:hover {
  background: #f0f0f0;
  border-color: var(--color-theme-1);
}

.keypad {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.keypad-button {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  padding: 15px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 5px;
  position: relative;
  overflow: hidden;
  transition: background-color 0.3s;
}

.keypad-button:active {
  background-color: #e0e0e0;
}

.keypad-button::after {
  content: '';
  display: block;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, #000 10%, transparent 10.01%);
  background-repeat: no-repeat;
  background-position: 50%;
  transform: scale(10, 10);
  opacity: 0;
  transition:
    transform 0.3s,
    opacity 0.5s;
}

.keypad-button:active::after {
  transform: scale(0, 0);
  opacity: 0.2;
  transition: 0s;
}

.button-content {
  position: relative;
  z-index: 1;
}

.keypad-button.done {
  background-color: var(--color-theme-1);
  color: white;
  grid-row: span 2;
}

.keypad-button.done:active {
  background-color: #45a049;
}

.keypad-button.backspace {
  color: var(--color-theme-1);
}

.keypad-button.backspace:active {
  background-color: #e8f5e9;
}

.keypad-button svg {
  width: 20px;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
}

.keypad-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.keypad-button:disabled:active {
  background-color: inherit;
}
</style> 