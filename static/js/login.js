
function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    firebase.auth().signInWithEmailAndPassword(email, password)
        // Successful logIn
        .then((userCredential) => {
            console.log("User logged in:", userCredential.user);
            window.location.replace("/students");  // Redirect to the students page
        })
        // Handling error
        .catch((error) => {
            errorMessage.innerHTML = error.message;
        });
}