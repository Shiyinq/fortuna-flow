<script lang="ts">
	import { onMount } from 'svelte';

	export let data;
	AnalyserNode;

	let amount = '0';
	let categoryId = '';
	let note = '';
	let transactionDate = '';
	let walletId = '';
	let amountInput: HTMLInputElement;
	let isFormValid = false;

	const categories = data.categories;

	const paymentMethods = data.wallets;

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
			categoryId !== '' &&
			transactionDate !== '' &&
			walletId !== '';
	};

	const handleKeypadInput = (value: string) => {
		switch (value) {
			case 'C':
				amount = '0';
				break;
			case 'DONE':
				if (isFormValid) {
					const formattedDate = new Date(transactionDate)
						.toISOString()
						.split('T')[0]
						.replace(/-/g, '/');
					console.log('Submitting form:', {
						amount,
						categoryId,
						note,
						transactionDate: formattedDate,
						walletId
					});
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
			handleKeypadInput('DONE');
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
		categoryId;
		transactionDate;
		walletId;
		validateForm();
	}

	onMount(() => {
		const today = new Date();
		transactionDate = today.toLocaleDateString('en-US', {
			weekday: 'long',
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		});

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

<div class="transaction-form">
	<h5>Add transaction</h5>
	<div class="form-content">
		<div class="amount-input">
			<span class="currency">IDR</span>
			<input
				type="text"
				bind:value={amount}
				on:keydown={handleKeyboardInput}
				on:paste={handlePaste}
				on:input={handleInput}
				bind:this={amountInput}
			/>
		</div>

		<div class="form-field">
			<span class="icon">🏷️</span>
			<select bind:value={categoryId} on:change={validateForm}>
				<option value="">Select category</option>
				{#each categories as cat}
					<option value={cat.categoryId}>{cat.categoryIcon ?? '💰'} {cat.name}</option>
				{/each}
			</select>
		</div>

		<div class="form-field">
			<span class="icon">📝</span>
			<input type="text" placeholder="Note" bind:value={note} />
		</div>

		<div class="form-field">
			<span class="icon">📅</span>
			<input type="date" bind:value={transactionDate} />
		</div>

		<div class="form-field">
			<span class="icon">💳</span>
			<select bind:value={walletId} on:change={validateForm}>
				<option value="">Select payment method</option>
				{#each paymentMethods as method}
					<option value={method.walletId}>{method.walletIcon ?? '💳'} {method.name}</option>
				{/each}
			</select>
		</div>

		<button
			class="save-button"
			class:active={isFormValid}
			on:click={() => handleKeypadInput('DONE')}
			disabled={!isFormValid}
		>
			Save
		</button>
	</div>

	<div class="keypad">
		{#each ['7', '8', '9', 'backspace', '4', '5', '6', 'C', '1', '2', '3', 'DONE', '0', '000', ','] as key}
			<button
				class="keypad-button"
				class:done={key === 'DONE'}
				class:backspace={key === 'backspace'}
				on:click={() => handleKeypadInput(key)}
				disabled={key === 'DONE' && !isFormValid}
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
</div>

<style>
	.transaction-form {
		font-family: Arial, sans-serif;
		max-width: 400px;
		margin: 0 auto;
		padding: 20px;
		border-radius: 8px;
		border: 1px solid var(--color-bg-0);
	}

	h5 {
		margin-top: 0;
	}

	.form-content {
		display: flex;
		flex-direction: column;
		gap: 15px;
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
		gap: 10px;
	}

	.icon {
		font-size: 20px;
	}

	input,
	select {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
	}

	select {
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M10.293 3.293L6 7.586 1.707 3.293A1 1 0 00.293 4.707l5 5a1 1 0 001.414 0l5-5a1 1 0 10-1.414-1.414z'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 10px center;
		padding-right: 30px;
	}

	.save-button {
		background-color: #e0e0e0;
		border: none;
		padding: 15px;
		border-radius: 5px;
		font-size: 18px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.save-button.active {
		background-color: var(--color-theme-1);
		color: white;
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

	.save-button:disabled,
	.keypad-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.save-button:disabled:active,
	.keypad-button:disabled:active {
		background-color: inherit;
	}
</style>
