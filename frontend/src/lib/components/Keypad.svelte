<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  export let disabledSave: boolean = false;
  const dispatch = createEventDispatcher();
  const keys = ['7', '8', '9', 'backspace', '4', '5', '6', 'C', '1', '2', '3', 'SAVE', '0', '000', ','];
  function handleClick(key: string) {
    dispatch('keypad', key);
  }
</script>
<div class="keypad">
  {#each keys as key}
    <button
      class="keypad-button"
      class:done={key === 'SAVE'}
      class:backspace={key === 'backspace'}
      on:click={() => handleClick(key)}
      disabled={key === 'SAVE' && disabledSave}
      type="button"
    >
      <span class="button-content">
        {#if key === 'backspace'}
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path><line x1="18" y1="9" x2="12" y2="15"></line><line x1="12" y1="9" x2="18" y2="15"></line></svg>
        {:else}
          {key}
        {/if}
      </span>
    </button>
  {/each}
</div>
<style>
.keypad {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 20px;
}
.keypad-button {
  display: flex;
  align-items: center;
  justify-content: center;
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
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}
.keypad-button.done {
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