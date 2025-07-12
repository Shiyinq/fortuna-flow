<script lang="ts">
	import cookie from 'cookie';
	import { token, currentLanguage, darkMode } from '$lib/store';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { useTranslation } from '$lib/i18n/useTranslation';
	import { availableLanguages, changeLanguage } from '$lib/i18n';

	import Heatmap from '$lib/components/charts/Heatmap.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';
	import Button from '$lib/components/Button.svelte';
	import MyCategories from '$lib/components/categories/MyCategories.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';
	import { logoutUser } from '$lib/apis/users';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
	import CardItem from '$lib/components/CardItem.svelte';
	import LanguageToggle from '$lib/components/LanguageToggle.svelte';

	const { t } = useTranslation();

	export let data: any;

	let activeTab = 'activities';
	let selectedLanguage = $currentLanguage;

	const getInitials = (name: string) => {
		if (!name) return '';
		return name.trim()[0].toUpperCase();
	};

	const logout = async () => {
		try {
			const currentToken = get(token);
			await logoutUser(currentToken);
		} catch (e) {
			console.error('Logout error', e);
		}
		const expiredToken = cookie.serialize('token', '', {
			path: '/',
			maxAge: -1
		});
		token.set('');
		document.cookie = expiredToken;
		goto('/auth/signin');
	};

	function handleLanguageChange(e: Event) {
		const lang = (e.target as HTMLSelectElement).value;
		selectedLanguage = lang;
		changeLanguage(lang);
	}
</script>

<svelte:head>
	<title>{$t('profile.title')}</title>
	<meta name="description" content="Fortuna Flow - {$t('profile.title')}" />
</svelte:head>

{#if data}
	<div class="profile-container">
		<Card className="profile-user" showGradient={true} marginTop={'0px'}>
			<div class="profile-info-centered">
				<div
					class="profile-picture-large"
					style={data.profile?.profilePicture
						? `background-image: url(${data.profile.profilePicture});`
						: ''}
				>
					{#if !data.profile?.profilePicture}
						<span class="profile-initial">{getInitials(data.profile?.name || 'U')}</span>
					{/if}
				</div>
				<h2 class="profile-name">{data.profile?.name || 'User'}</h2>
				<p class="username-profile-centered">@{data.profile?.username || 'username'}</p>
			</div>
			<div class="profile-shortcuts">
				<button
					class="ig-tab {activeTab === 'activities' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'activities')}
				>
					<span class="ig-tab-icon">📊</span>
					<span class="ig-tab-label">{$t('profile.activities') || 'Aktivitas'}</span>
				</button>
				<button
					class="ig-tab {activeTab === 'wallets' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'wallets')}
				>
					<span class="ig-tab-icon">💼</span>
					<span class="ig-tab-label">{$t('navigation.wallets') || 'Dompet'}</span>
				</button>
				<button
					class="ig-tab {activeTab === 'categories' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'categories')}
				>
					<span class="ig-tab-icon">📂</span>
					<span class="ig-tab-label">{$t('navigation.categories') || 'Kategori'}</span>
				</button>
				<button
					class="ig-tab {activeTab === 'settings' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'settings')}
				>
					<span class="ig-tab-icon">⚙️</span>
					<span class="ig-tab-label">{$t('profile.settings') || 'Pengaturan'}</span>
				</button>
			</div>
		</Card>

		{#if activeTab === 'activities'}
			<Card
				className="activity-user"
				title={$t('profile.activitiesHistory')}
				showGradient={true}
				marginTop={'0px'}
				highlightTitle={true}
			>
				{#each data.activities || [] as activity}
					<Heatmap
						data={activity.transactions}
						startDate={activity.startDate}
						endDate={activity.endDate}
					/>
				{/each}
			</Card>
		{:else if activeTab === 'wallets'}
			<MyWallets
				wallets={data.wallets || []}
				title={$t('wallets.myWallets')}
				subtitle={$t('wallets.newWallet')}
				subtitleLink="/wallets/create"
				showGradient={true}
				marginTop={'0px'}
				marginBottom={'0px'}
			/>
		{:else if activeTab === 'categories'}
			<MyCategories categories={data.categories} />
		{:else if activeTab === 'settings'}
			<Card title={$t('profile.settings') || 'Pengaturan'} showGradient={true} marginTop={'0px'} highlightTitle={true}>
				<div class="settings-container">
					<div class="setting-item">
						<label for="language-toggle" class="setting-label">{$t('profile.language') || 'Bahasa'}</label>
						<LanguageToggle />
					</div>
					
					<div class="setting-item">
						<label for="darkmode-toggle" class="setting-label">{$t('profile.theme') || 'Tema'}</label>
						<DarkModeToggle />
					</div>
					
					<div class="setting-item">
						<Button variant="danger" fullWidth className="logout-btn-setting" on:click={logout}>
							{$t('auth.signout') || 'Keluar'}
						</Button>
					</div>
				</div>
			</Card>
		{/if}
		<br />
	</div>
{:else}
	<div class="profile-container">
		<LoadingState message={$t('common.loading')} />
	</div>
{/if}

<style>
	.profile-container {
		width: 100%;
		display: flex;
		margin: 0 auto;
		max-width: 100%;
		align-items: center;
		flex-direction: column;
	}

	.profile-info-centered {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 0px 0 12px 0;
	}
	.profile-picture-large {
		width: 100px;
		height: 100px;
		border-radius: 50%;
		background-color: var(--color-bg-2);
		background-size: cover;
		background-position: center;
		margin-bottom: 16px;
		box-shadow: 0 2px 8px var(--glassy-shadow-light);
	}
	.profile-name {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-theme-1);
		text-align: center;
	}
	.username-profile-centered {
		font-size: 1rem;
		font-weight: 500;
		margin: 4px 0 0 0;
		letter-spacing: 0.2px;
		color: var(--color-text-secondary);
		text-align: center;
	}
	.profile-shortcuts {
		display: flex;
		gap: 36px;
		justify-content: center;
		margin: 24px 0 0 0;
		border-bottom: 1.5px solid var(--glassy-border);
		padding-bottom: 2px;
	}
	.ig-tab {
		border: none;
		background: none;
		outline: none;
		box-shadow: none;
		appearance: none;
		cursor: pointer;
		color: var(--color-text-secondary);
	}
	.ig-tab:focus {
		outline: 2px solid var(--color-success);
		outline-offset: 2px;
	}
	.ig-tab:focus:not(:focus-visible) {
		outline: none;
	}
	.ig-tab-icon {
		font-size: 1.3rem;
		margin-bottom: 2px;
		line-height: 1;
	}
	.ig-tab-label {
		font-size: 0.93rem;
		font-weight: 600;
		color: inherit;
		letter-spacing: 0.2px;
		text-align: center;
		transition: color 0.18s;
	}
	.ig-tab.active {
		color: var(--color-success);
	}
	.ig-tab.active .ig-tab-label {
		color: var(--color-success);
	}
	.profile-initial {
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 2.2rem;
		font-weight: 700;
		color: var(--color-bg-2);
		width: 100%;
		height: 100%;
		background: var(--color-success);
		border-radius: 50%;
		user-select: none;
	}

	.settings-container {
		display: flex;
		flex-direction: column;
		gap: 24px;
		padding: 8px 0;
	}

	.setting-item {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.setting-label {
		font-weight: 600;
		font-size: 0.95rem;
		color: var(--color-text-primary);
		margin: 0;
	}

	.logout-btn-setting {
		margin-top: 8px;
	}
</style>
