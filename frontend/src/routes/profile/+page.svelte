<script lang="ts">
	import cookie from 'cookie';
	import { token } from '$lib/store';
	import { goto } from '$app/navigation';

	import Heatmap from '$lib/components/charts/Heatmap.svelte';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';
	import Button from '$lib/components/Button.svelte';
	import MyCategories from '$lib/components/categories/MyCategories.svelte';
	import MyWallets from '$lib/components/wallets/MyWallets.svelte';

	export let data: any;

	let activeTab = 'activities';

	const getInitials = (name: string) => {
		if (!name) return '';
		return name.trim()[0].toUpperCase();
	};

	const logout = () => {
		const expiredToken = cookie.serialize('token', '', {
			path: '/',
			maxAge: -1
		});

		token.set('');
		document.cookie = expiredToken;

		goto('/auth/signin');
	};
</script>

<svelte:head>
	<title>Profile</title>
	<meta name="description" content="Fortuna Flow - Profile" />
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
			<div class="profile-shortcuts-ig">
				<button
					class="ig-tab {activeTab === 'activities' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'activities')}
				>
					<span class="ig-tab-icon">📊</span>
					<span class="ig-tab-label">Activities</span>
				</button>
				<button
					class="ig-tab {activeTab === 'wallets' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'wallets')}
				>
					<span class="ig-tab-icon">💼</span>
					<span class="ig-tab-label">Wallets</span>
				</button>
				<button
					class="ig-tab {activeTab === 'categories' ? 'active' : ''}"
					type="button"
					tabindex="0"
					on:click={() => (activeTab = 'categories')}
				>
					<span class="ig-tab-icon">📂</span>
					<span class="ig-tab-label">Categories</span>
				</button>
			</div>
		</Card>

		{#if activeTab === 'activities'}
			<Card
				className="activity-user"
				title="Activities History"
				showGradient={true}
				marginTop={'0px'}
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
				title="My Wallets"
				subtitle="Create New Wallet"
				subtitleLink="/wallets/create"
				showGradient={true}
				marginTop={'0px'}
				marginBottom={'0px'}
			/>
		{:else if activeTab === 'categories'}
			<MyCategories categories={data.categories} />
		{/if}
		<br />
		<Button variant="danger" fullWidth on:click={logout}>Logout</Button>
	</div>
{:else}
	<div class="profile-container">
		<LoadingState message="Please wait while we load your profile." />
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
		padding: 24px 0 12px 0;
	}
	.profile-picture-large {
		width: 100px;
		height: 100px;
		border-radius: 50%;
		background-color: #eee;
		background-size: cover;
		background-position: center;
		margin-bottom: 16px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
	}
	.profile-name {
		margin: 0;
		font-size: 1.5rem;
		font-weight: 700;
		color: var(--color-theme-1, #222);
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
	.profile-shortcuts-ig {
		display: flex;
		gap: 36px;
		justify-content: center;
		margin: 18px 0 0 0;
		border-bottom: 1.5px solid #e5e7eb;
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
		outline: 2px solid #1dbf73;
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
		color: #1dbf73;
	}
	.ig-tab.active .ig-tab-label {
		color: #1dbf73;
	}
	.profile-initial {
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 2.2rem;
		font-weight: 700;
		color: #fff;
		width: 100%;
		height: 100%;
		background: #1dbf73;
		border-radius: 50%;
		user-select: none;
	}
</style>
