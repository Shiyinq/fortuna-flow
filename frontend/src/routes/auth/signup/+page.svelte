<script>
	import '../auth.css';
</script>

<div class="auth sign-in">
	<form class="form">
		<h1>Sign up</h1>
		<p>Create an account before sign in</p>
		<div class="form-field">
			<input
				class="nb-input default"
				type="text"
				name="name"
				id="name"
				placeholder="Enter your name"
			/>
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="text"
				name="username"
				id="username"
				placeholder="Enter your username"
			/>
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="email"
				name="email"
				id="email"
				placeholder="Enter your email"
			/>
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="password"
				name="password"
				id="password"
				placeholder="Enter your password"
			/>
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="password"
				name="confirm-password"
				id="confirm-password"
				placeholder="Re enter your password"
			/>
		</div>
		<div class="form-button">
			<button class="nb-button default" type="submit" name="signin">Sign in</button>
		</div>
		<p class="link-auth">
			Already have an account? <a href="/auth/signin">Sign in</a>
		</p>
	</form>
</div>

<style>
	.auth {
		height: 80vh;
		display: flex;
		justify-content: center;
	}
</style>
