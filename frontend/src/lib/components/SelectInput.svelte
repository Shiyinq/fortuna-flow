<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let value: string = '';
  export let label: string = '';
  export let icon: string = '';
  export let options: Array<{ value: string, label: string, icon?: string } > = [];
  export let required: boolean = false;
  export let disabled: boolean = false;
  export let placeholder: string = '';
  export let showManageButton: boolean = false;
  export let manageLabel: string = '';
  export let onManage: (() => void) | null = null;

  const dispatch = createEventDispatcher();
  function handleChange(e: Event) {
    const target = e.target as HTMLSelectElement;
    dispatch('change', target.value);
  }
  function handleManage() {
    if (onManage) onManage();
  }
</script>

<div class="form-field">
  {#if icon}
    <span class="icon">{icon}</span>
  {/if}
  <select bind:value {required} {disabled} aria-label={label} on:change={handleChange} class="form-input">
    <option value="" disabled>{placeholder}</option>
    {#each options as opt}
      <option value={opt.value}>{opt.icon ? `${opt.icon} ` : ''}{opt.label}</option>
    {/each}
  </select>
  {#if showManageButton && onManage}
    <button class="manage-button" type="button" on:click={handleManage}>{manageLabel}</button>
  {/if}
</div>

<style>
.form-field {
  display: flex;
  align-items: center;
  gap: 10px;
}
.icon {
  font-size: 20px;
}
.form-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
}
.manage-button {
  background: #fff !important;
  border: 1px solid #e0e0e0 !important;
  color: #222 !important;
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
:global(:root.dark) .manage-button {
  background: rgba(30, 41, 59, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #f1f5f9 !important;
}
.manage-button:hover {
  background: #f0f0f0 !important;
  border-color: var(--color-theme-1) !important;
}
:global(:root.dark) .manage-button:hover {
  background: rgba(30, 41, 59, 0.9) !important;
}
</style> 