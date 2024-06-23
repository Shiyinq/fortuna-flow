<script>
    import { goto } from '$app/navigation';
	import { token } from '$lib/store';
    import { onMount } from 'svelte';

    onMount(() => {
        const params = new URLSearchParams(window.location.search);
        const access_token = params.get('access_token');

        if (access_token) {
            token.set(access_token);
            goto('/');
        } else {
            goto('/auth/signin');
        }
    });
</script>

<p class="check-callback">Authenticating...</p>

<style>
    .check-callback {
        height: 50vh;
        display: flex;
        text-align: center;
        align-items: center;
        justify-content: center;
    }
</style>