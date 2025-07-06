<script lang="ts">
	import cookie from 'cookie';
	import { token } from '$lib/store';
	import { goto } from '$app/navigation';

	import Heatmap from '$lib/components/charts/Heatmap.svelte';
	import defaultUserProfilePicture from '$lib/images/defaultUserProfilePicture.svg';
	import LoadingState from '$lib/components/LoadingState.svelte';
	import Card from '$lib/components/Card.svelte';
	import Button from '$lib/components/Button.svelte';

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

{#if data}
	<div class="profile-container">
		<Card className="profile-user" title="My Profile" showGradient={true} marginTop={"0px"}>
			<div class="profile-info glassy-light">
				<div>
					<h2><b>{data.profile?.name || 'User'}</b></h2>
					<p>{data.profile?.username || 'username'}</p>
				</div>
				<div
					class="profile-picture"
					style="background-image: url({getProfilePicture(data.profile || {})});"
				></div>
			</div>
		</Card>

		<Card className="activity-user" title="Activities History" showGradient={true} marginTop={"0px"}>
			{#each data.activities || [] as activity}
				<Heatmap
					data={activity.transactions}
					startDate={activity.startDate}
					endDate={activity.endDate}
				/>
			{/each}
		</Card>
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
		padding: 15px;
		border-radius: 10px;
		align-items: center;
		justify-content: space-between;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	}

	.profile-info:hover {
		transform: translateY(-1px);
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
</style>
