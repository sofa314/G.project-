const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const loginForm = document.querySelector('.login form');
    const signupForm = document.querySelector('.signup form');
    const forgotPasswordLink = document.querySelector('.forgot-password');

    // Handle login form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        const password = this.querySelector('input[type="password"]').value;

        // Here you would typically make an API call to verify credentials
        // For now, we'll just simulate a successful login
        localStorage.setItem('isLoggedIn', 'true');
        window.location.href = 'index.html';
    });

    // Handle signup form submission
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = this.querySelector('input[type="text"]').value;
        const email = this.querySelector('input[type="email"]').value;
        const password = this.querySelector('input[type="password"]').value;

        // Here you would typically make an API call to create a new account
        // For now, we'll just simulate a successful signup
        localStorage.setItem('isLoggedIn', 'true');
        window.location.href = 'index.html';
    });

    // Handle forgot password
    forgotPasswordLink.addEventListener('click', function(e) {
        e.preventDefault();
        const email = loginForm.querySelector('input[type="email"]').value;
        
        if (!email) {
            alert('Please enter your email address first');
            return;
        }

        // Here you would typically make an API call to send a password reset email
        alert('Password reset instructions have been sent to your email');
    });
});

function handleCredentialResponse(response) {
    // Get the ID token from the response
    const credential = response.credential;
    
    // Decode the JWT token to get user information
    const payload = JSON.parse(atob(credential.split('.')[1]));
    
    // You can now use the user information
    console.log('User email:', payload.email);
    console.log('User name:', payload.name);
    
    // Here you would typically:
    // 1. Send the credential to your backend
    // 2. Verify the token
    // 3. Create or update the user in your database
    // 4. Create a session for the user
    // 5. Redirect to the appropriate page
    
    // For now, we'll just redirect to the home page
    window.location.href = 'index.html';
}