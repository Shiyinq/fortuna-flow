<script lang="ts">
	import { onMount } from 'svelte';
	import { Toaster, toast } from 'svelte-sonner';

	import { convertToInteger } from '$lib/utils';
	import { addWallet } from '$lib/apis/wallets';
	import { initialTransactionSelected, token, transactionSelected } from '$lib/store/index.js';
	import IconSelector from '$lib/components/IconSelector.svelte';
	import Card from '$lib/components/Card.svelte';
	import { WALLET_ICONS } from '$lib/constants';
	import AmountInput from '$lib/components/AmountInput.svelte';
	import TextInput from '$lib/components/TextInput.svelte';
	import Keypad from '$lib/components/Keypad.svelte';
	import Button from '$lib/components/Button.svelte';

	AnalyserNode;

	export let walletId = '';
	export let balance = ''.replace(/[^0-9.,]/g, '');
	export let name = '';
	export let typeForm = 'edit';
	export let walletIcon = '';

	let isFormValid = false;

	const createWallet = async () => {
		try {
			let response = await addWallet(
				$token,
				name,
				convertToInteger(balance),
				walletIcon
			);
			toast.success(response.detail);
			walletId = '';
			balance = '';
			name = '';
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
		const unformatNumber = (num: string) => num.replace(/\./g, '');
		const formatNumber = (num: string) => {
			const parts = num.split(',');
			parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
			return parts.join(',');
		};
		switch (value) {
			case 'C':
				balance = '';
				break;
			case 'backspace': {
				const unformatted = unformatNumber(balance);
				if (unformatted.length > 1) {
					balance = formatNumber(unformatted.slice(0, -1));
				} else {
					balance = '';
				}
				break;
			}
			default:
				balance = formatNumber(unformatNumber(balance) + value);
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

	$: {
		balance;
		name;
		validateForm();
	}

	onMount(() => {
		if (typeForm === 'create') {
			transactionSelected.set(initialTransactionSelected);
		}
		validateForm();
	});
</script>

<Toaster richColors position="top-center" />
<Card title={walletId ? 'Edit Wallet' : 'Add Wallet'} showGradient={true} className="wallet-form" marginTop="0" marginBottom="0" highlightTitle={true}>
	<div class="form-content">
		<AmountInput
		  bind:value={balance}
		  placeholder="0"
		  disabled={false}
		  on:change={(e) => { balance = e.detail; validateForm(); }}
		/>
		<TextInput
		  bind:value={name}
		  icon="📝"
		  placeholder="Name"
		  maxlength={50}
		  required={true}
		  on:change={(e) => { name = e.detail; validateForm(); }}
		/>
		<IconSelector bind:selectedIcon={walletIcon} icons={WALLET_ICONS} label="🎨" />
	</div>
	<div class="keypad-margin-bottom">
		<Keypad on:keypad={e => handleKeypadInput(e.detail)} />
	</div>
	<Button variant="primary-solid" fullWidth on:click={createWallet} disabled={!isFormValid} className="save-btn-margin">
		Save
	</Button>
</Card>

<style>
.keypad-margin-bottom {
	margin-bottom: 20px;
}
</style>
