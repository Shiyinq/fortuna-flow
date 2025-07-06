<script lang="ts">
	import { onMount } from 'svelte';
	import { Toaster, toast } from 'svelte-sonner';

	import { convertToInteger } from '$lib/utils';
	import { addWallet } from '$lib/apis/wallets';
	import { initialTransactionSelected, token, transactionSelected } from '$lib/store/index.js';

	AnalyserNode;

	export let walletId = '';
	export let balance = ''.replace(/[^0-9.,]/g, '');
	export let name = '';
	export let typeForm = 'edit';

	let isFormValid = false;
	let amountInput: HTMLInputElement;
	let walletIcon = '';

	const walletIcons = [
		'💳', '🏦', '💰', '💎', '🏆', '⭐', '💡', '🎯', '🚀', '🌟',
		'💼', '🎁', '🎉', '🏅', '🥇', '🥈', '🥉', '💎', '🔮', '🎪',
		'🎨', '🎭', '🎪', '🎯', '🎲', '🎮', '🎸', '🎹', '🎺', '🎻'
	];

	const createWallet = async () => {
		try {
			let response = await addWallet($token, name, convertToInteger(balance), walletIcon || undefined);
			toast.success(response.detail);
			walletId = '';
			balance = '';
			name = '';
			walletIcon = '';
		} catch (error: any) {
			toast.error(error.detail);
		}
	};

	const formatNumber = (num: string): string => {
		const parts = num.split(',');
		parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
		return parts.join(',');
	};

	const unformatNumber = (num: string): string => {
		return num.replace(/\./g, '');
	};

	const updateAmount = (value: string) => {
		const unformattedAmount = unformatNumber(balance);
		if (unformattedAmount === '0' && value !== '000' && value !== ',') {
			balance = formatNumber(value);
		} else {
			balance = formatNumber(unformatNumber(balance) + value);
		}
	};

	const handleBackspace = () => {
		const unformattedAmount = unformatNumber(balance);
		if (unformattedAmount.length > 1) {
			balance = formatNumber(unformattedAmount.slice(0, -1));
		} else {
			balance = '0';
		}
	};

	const validateForm = () => {
		isFormValid = unformatNumber(balance) !== '0' && name !== '';
	};

	const handleKeypadInput = async (value: string) => {
		switch (value) {
			case 'C':
				balance = '0';
				break;
			case 'SAVE':
				if (isFormValid) {
					if (walletId) {
						return;
					} else {
						await createWallet();
					}
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
		const unformattedAmount = unformatNumber(balance);
		balance = formatNumber(unformattedAmount);
		validateForm();
	};

	const selectIcon = (icon: string) => {
		walletIcon = walletIcon === icon ? '' : icon;
	};

	$: {
		balance;
		name;
		validateForm();
	}

	onMount(() => {
		if (typeForm === 'create') {
			transactionSelected.set(initialTransactionSelected);
		}
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

<Toaster richColors position="top-center" />
<div class="wallet-form">
	<div class="form-header">
		<h5>{walletId ? 'Edit Wallet' : 'Add Wallet'}</h5>
	</div>
	<div class="form-content">
		<div class="balance-input">
			<span class="currency">IDR</span>
			<input
				type="text"
				placeholder="0"
				bind:value={balance}
				on:keydown={handleKeyboardInput}
				on:paste={handlePaste}
				on:input={handleInput}
				bind:this={amountInput}
			/>
		</div>

		<div class="form-field">
			<span class="icon">📝</span>
			<input type="text" placeholder="Name" bind:value={name} />
		</div>

		<div class="icon-selection">
			<span class="icon">🎨</span>
			<div class="icon-grid">
				{#each walletIcons as icon}
					<button
						type="button"
						class="icon-option {walletIcon === icon ? 'selected' : ''}"
						on:click={() => selectIcon(icon)}
					>
						{icon}
					</button>
				{/each}
			</div>
			{#if walletIcon}
				<div class="selected-icon">
					Selected: <span class="icon">{walletIcon}</span>
					<button type="button" class="clear-icon" on:click={() => walletIcon = ''}>
						Clear
					</button>
				</div>
			{/if}
		</div>
	</div>

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
</div>

<style>
	.wallet-form {
		font-family: Arial, sans-serif;
		max-width: 400px;
		margin: 0 auto;
		padding: 20px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
	}

	.form-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0 0 16px 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	.form-content {
		display: flex;
		flex-direction: column;
		gap: 15px;
	}

	.balance-input {
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

	input {
		width: 100%;
		padding: 10px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		font-size: 16px;
	}

	.icon-selection {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.icon-grid {
		display: grid;
		grid-template-columns: repeat(10, 1fr);
		gap: 5px;
	}

	.icon-option {
		width: 30px;
		height: 30px;
		border: 1px solid #e0e0e0;
		border-radius: 5px;
		background: #ffffff;
		cursor: pointer;
		font-size: 14px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: background-color 0.3s;
	}

	.icon-option:hover {
		border-color: var(--color-theme-1);
		background: #f0f0f0;
	}

	.icon-option.selected {
		border-color: var(--color-theme-1);
		background: var(--color-theme-1);
		color: white;
	}

	.selected-icon {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px;
		background: #f0f0f0;
		border-radius: 5px;
		font-size: 12px;
	}

	.clear-icon {
		background: none;
		border: none;
		color: #ff4444;
		cursor: pointer;
		font-size: 11px;
		text-decoration: underline;
	}

	.clear-icon:hover {
		color: #ff4444;
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
