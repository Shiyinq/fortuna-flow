<script lang="ts">
	import cookie from 'cookie';
	import { token } from '$lib/store';
	import { goto } from '$app/navigation';
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
	<div
		class="profile-picture"
		style="background-image: url({getProfilePicture(data.profile)});"
	></div>
	<div class="profile-info">
		<h2>{data.profile.username}</h2>
		<p>{data.profile.email}</p>
	</div>
	<button class="logout-button" on:click={logout}>Logout</button>
</div>

<style>
	.profile-container {
		width: 100%;
		padding: 20px;
		display: flex;
		margin: 0 auto;
		max-width: 100%;
		border-radius: 10px;
		align-items: center;
		flex-direction: column;
		border: 1px solid var(--color-bg-0);
	}

	.profile-picture {
		width: 100px;
		height: 100px;
		border-radius: 50%;
		margin-bottom: 20px;
		background-size: auto;
		background-color: #eee;
		background-position: center;
	}

	.profile-info {
		text-align: center;
	}

	.profile-info h2 {
		margin: 0;
		font-size: 24px;
	}

	.profile-info p {
		margin: 5px 0;
		color: #666;
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
