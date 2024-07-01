<script lang="ts">
	import cookie from 'cookie';
	import { token } from '$lib/store';
	import { goto } from '$app/navigation';

	import Heatmap from '$lib/components/charts/Heatmap.svelte';
	import defaultUserProfilePicture from '$lib/images/defaultUserProfilePicture.svg';

	export let data: any;

	const getProfilePicture = (user: any) => {
		return user.profilePicture ? user.profilePicture : defaultUserProfilePicture;
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

<div class="profile-container">
	<div class="profile-info">
		<div>
			<h2><b>{data.profile.name}</b></h2>
			<p>{data.profile.username}</p>
		</div>
		<div
			class="profile-picture"
			style="background-image: url({getProfilePicture(data.profile)});"
		></div>
	</div>
	<button class="logout-button" on:click={logout}>Logout</button>

	<div class="activity-user">
		<div class="activity-user-header">
			<h5>Activities History</h5>
		</div>
		{#each data.activities as activity }
			<Heatmap data={activity.transactions} startDate={activity.startDate} endDate={activity.endDate}/>
		{/each}
	</div>
</div>

<style>
	.activity-user {
		width: 100%;
		padding: 10px;
		margin-top: 16px;
		border-radius: 10px;
		border: 1px solid var(--color-bg-0);
	}

	.activity-user-header h5 {
		margin: 0;
		margin-top: 8px;
	}

	.profile-container {
		width: 100%;
		padding: 10px;
		display: flex;
		margin: 0 auto;
		max-width: 100%;
		border-radius: 10px;
		align-items: center;
		flex-direction: column;
	}

	.profile-container button {
		width: 100%;
	}

	.profile-picture {
		width: 80px;
		height: 80px;
		border-radius: 50%;
		margin-bottom: 20px;
		background-color: #eee;
		background-size: 80px 80px;
		background-position: center;
	}

	.profile-info {
		width: 100%;
		display: flex;
		padding: 10px;
		border-radius: 10px;
		align-items: center;
		justify-content: space-between;
		border: 1px solid var(--color-bg-0);
	}

	.profile-info h2 {
		margin: 0;
		font-size: 24px;
	}

	.profile-info p {
		color: #666;
		margin: 5px 0;
		font-size: 20px;
	}

	.logout-button {
		padding: 10px 20px;
		font-size: 16px;
		font-weight: bold;
		color: white;
		background-color: #ff6b6b;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition:
			background-color 0.3s,
			transform 0.3s;
		margin-top: 20px;
	}

	.logout-button:hover {
		background-color: #ff4c4c;
		transform: scale(1.05);
	}

	.logout-button:active {
		background-color: #e24444;
	}
</style>
