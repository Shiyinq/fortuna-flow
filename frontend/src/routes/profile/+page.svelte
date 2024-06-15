<script>
	import { goto } from '$app/navigation';
	import defaultUserProfilePicture from '$lib/images/defaultUserProfilePicture.svg';

	let user = {
		userId: 'b1831218-5175-411e-868e-3fe72d76da75',
		profilePicture: null,
		email: 'shiyinq@mymail.com',
		username: 'Shiyinq'
	};

	const getProfilePicture = () => {
		return user.profilePicture ? user.profilePicture : defaultUserProfilePicture;
	};

	const logout = () => {
		goto("/auth/signin");
	};
</script>

<svelte:head>
	<title>Profile</title>
	<meta name="description" content="Fortuna Flow - Profile" />
</svelte:head>

<div class="profile-container">
	<div class="profile-picture" style="background-image: url({getProfilePicture()});"></div>
	<div class="profile-info">
		<h2>{user.username}</h2>
		<p>{user.email}</p>
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
		border: 1px solid #fff;
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
