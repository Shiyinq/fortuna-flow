<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';

  export let value: string = '0';
  export let disabled: boolean = false;
  export let placeholder: string = '0';
  export let inputRef: HTMLInputElement | null = null;

  const dispatch = createEventDispatcher();

  // Format number to IDR style
  function formatNumber(num: string): string {
    const parts = num.split(',');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return parts.join(',');
  }
  function unformatNumber(num: string): string {
    return num.replace(/\./g, '');
  }

  function updateAmount(val: string) {
    const unformatted = unformatNumber(value);
    if (unformatted === '0' && val !== '000' && val !== ',') {
      value = formatNumber(val);
    } else {
      value = formatNumber(unformatNumber(value) + val);
    }
    dispatch('change', value);
  }
  function handleBackspace() {
    const unformatted = unformatNumber(value);
    if (unformatted.length > 1) {
      value = formatNumber(unformatted.slice(0, -1));
    } else {
      value = '0';
    }
    dispatch('change', value);
  }
  function handleKeypadInput(val: string) {
    if (disabled) return;
    switch (val) {
      case 'C':
        value = '0';
        break;
      case 'backspace':
        handleBackspace();
        break;
      default:
        updateAmount(val);
    }
    dispatch('change', value);
    dispatch('keypad', val);
  }
  function handleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    const unformatted = unformatNumber(target.value);
    value = formatNumber(unformatted);
    dispatch('change', value);
  }
  function handlePaste(e: ClipboardEvent) {
    e.preventDefault();
    const pasted = e.clipboardData?.getData('text') || '';
    const sanitized = pasted.replace(/[^0-9,]/g, '');
    value = formatNumber(sanitized);
    dispatch('change', value);
  }
  function handleKeyboardInput(e: KeyboardEvent) {
    if (!/^[0-9,]$/.test(e.key) && !['Backspace', 'ArrowLeft', 'ArrowRight', 'Tab'].includes(e.key)) {
      e.preventDefault();
    }
    if (e.key === 'Backspace') handleBackspace();
  }
  onMount(() => {
    if (inputRef) {
      inputRef.addEventListener('focus', () => {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
          inputRef && inputRef.blur();
        }
      });
    }
  });
</script>

<div class="amount-input">
  <span class="currency">IDR</span>
  <input
    type="text"
    bind:value
    {placeholder}
    {disabled}
    on:input={handleInput}
    on:paste={handlePaste}
    on:keydown={handleKeyboardInput}
    bind:this={inputRef}
    class="form-input"
  />
</div>

<style>
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
.form-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
}
</style> 