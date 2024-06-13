<script>
	import '../auth.css';
</script>

<div class="auth sign-in">
	<form class="form">
		<h1>Sign in</h1>
		<p>Welcome to Fotuna Flow</p>
		<div class="form-field">
			<input
				class="nb-input default"
				type="text"
				name="username"
				id="username"
				placeholder="Username"
			/>
		</div>
		<div class="form-field">
			<input
				class="nb-input default"
				type="password"
				name="password"
				id="password"
				placeholder="Password"
			/>
		</div>
		<div class="form-button">
			<button class="nb-button default" type="submit" name="signin">Sign in</button>
		</div>
		<p class="link-auth">
			Don't have an account? <a href="/auth/signup">Sign up</a>
		</p>
	</form>
</div>
