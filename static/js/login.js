function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Check if the email domain is allowed - only @admin
    if (email.endsWith('@admin.com')) {
        // Sign in with email and password
        firebase.auth().signInWithEmailAndPassword(email, password)
            .then((userCredential) => {
                console.log("User logged in:", userCredential.user);
                window.location.replace("/students");  
            })
            // Handling error
            .catch((error) => {
                errorMessage.innerHTML = error.message;
            });
    } else {
        // Display error message for unauthorized users
        errorMessage.innerHTML = "Only administrators are allowed to access this website.";
    }
}

