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
	<div class="profile-user">
		<div class="profile-user-header">
			<h5>My Profile</h5>
		</div>
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
	</div>

	<div class="activity-user">
		<div class="activity-user-header">
			<h5>Activities History</h5>
		</div>
		{#each data.activities as activity}
			<Heatmap
				data={activity.transactions}
				startDate={activity.startDate}
				endDate={activity.endDate}
			/>
		{/each}
	</div>
	<br />
	<button class="logout-button" on:click={logout}>Logout</button>
</div>

<style>
	.profile-user,
	.activity-user {
		width: 100%;
		padding: 20px;
		margin-top: 16px;
		border-radius: 16px;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255,255,255,0.3);
		box-shadow: 0 8px 32px rgba(180, 200, 220, 0.15);
	}

	.activity-user-header h5,
	.profile-user-header h5 {
		font-size: 1.2rem;
		font-weight: 600;
		margin: 0 0 16px 0;
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
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

	.profile-user {
		margin-top: -10px;
	}

	.profile-info {
		width: 100%;
		display: flex;
		padding: 15px;
		margin-top: 16px;
		border-radius: 10px;
		align-items: center;
		background: rgba(255,255,255,0.6);
		backdrop-filter: blur(6px);
		border: none;
		box-shadow: 0 2px 8px rgba(180, 200, 220, 0.08);
		justify-content: space-between;
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
