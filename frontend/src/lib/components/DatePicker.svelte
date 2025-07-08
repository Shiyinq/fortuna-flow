<script lang="ts">
  import flatpickr from 'flatpickr';
  import 'flatpickr/dist/flatpickr.min.css';
  import { onMount, onDestroy } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import { tick } from 'svelte';

  export let value: string = '';
  export let placeholder: string = 'dd/mm/yyyy';
  export let disabled: boolean = false;
  export let options: any = {};

  const dispatch = createEventDispatcher();
  let inputEl: HTMLInputElement;
  let fp: flatpickr.Instance | null = null;
  let observer: MutationObserver;

  let isDark = false;
  function updateTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  onMount(async () => {
    await tick();
    updateTheme();
    fp = flatpickr(inputEl, {
      dateFormat: 'Y-m-d',
      defaultDate: value || undefined,
      disableMobile: true,
      ...options,
      onChange: (selectedDates, dateStr) => {
        value = dateStr;
        dispatch('change', dateStr);
      },
      onReady: () => {
        updateTheme();
      }
    });
    observer = new MutationObserver(() => updateTheme());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
  });

  onDestroy(() => {
    fp?.destroy();
    observer?.disconnect();
  });
</script>

<div class="datepicker-wrapper {isDark ? 'dark' : ''}">
  <input
    bind:this={inputEl}
    type="text"
    class="datepicker-input"
    {placeholder}
    bind:value
    {disabled}
    readonly
    autocomplete="off"
  />
</div>

<style>
.datepicker-wrapper {
  width: 100%;
}
.datepicker-input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--glassy-border);
  border-radius: 5px;
  font-size: 16px;
  background: var(--color-bg-2);
  color: var(--color-text-strong);
  outline: none;
  transition: border 0.2s;
}
.datepicker-input:focus {
  border: 1.5px solid var(--color-theme-1);
}
</style> 