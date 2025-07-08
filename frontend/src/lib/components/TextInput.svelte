<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let value: string = '';
  export let label: string = '';
  export let icon: string = '';
  export let placeholder: string = '';
  export let maxlength: number = 50;
  export let required: boolean = false;
  export let disabled: boolean = false;

  const dispatch = createEventDispatcher();
  function handleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    dispatch('change', target.value);
  }
</script>

<div class="form-field">
  {#if icon}
    <span class="icon">{icon}</span>
  {/if}
  <input
    type="text"
    bind:value
    {placeholder}
    {maxlength}
    {required}
    {disabled}
    aria-label={label}
    on:input={handleInput}
    class="form-input"
  />
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
}
</style> 