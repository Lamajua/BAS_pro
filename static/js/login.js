
function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            // Redirect or handle successful login
            console.log("User logged in:", userCredential.user);
            window.location.replace("/students");  // Redirect to a dashboard page
        })
        .catch((error) => {
            // Handle errors
            errorMessage.innerHTML = error.message;
        });
}