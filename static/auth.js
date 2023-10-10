const firebaseConfig = {
    apiKey: "AIzaSyBwcg6jP6zuqzdyo8vXJFp3vLc8xWEeFvY",
    authDomain: "anpr-5a023.firebaseapp.com",
    databaseURL: "https://anpr-5a023-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "anpr-5a023",
    storageBucket: "anpr-5a023.appspot.com",
    messagingSenderId: "345044990316",
    appId: "1:345044990316:web:6df59ec38da2b603145b49",
    measurementId: "G-M177D7SBVV"
};


const app = firebase.initializeApp(firebaseConfig);
const auth = app.auth();

// Sign in (example with email & password)
function signIn(email, password) {
    auth.signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            const user = userCredential.user;
            user.getIdToken().then(function(token) {
                // Send this token to your Flask backend for verification
                sendTokenToServer(token);
            });
        })
        .catch((error) => {
            console.error("Error signing in", error);
        });
}

function sendTokenToServer(token) {
    fetch('/verify-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({token: token})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log("Token verified!");
            // Proceed with your application logic
        } else {
            console.error("Token verification failed:", data.message);
        }
    });
}
