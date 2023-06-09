

const messaging = firebase.messaging();
console.log("messaging initialized")
function requestNotificationPermission() {
  messaging
    .requestPermission()
    .then(() => {
      console.log("Notification permission granted.");
      // Handle permission granted
    })
    .catch((error) => {
      console.log("Unable to get permission to notify.", error);
      // Handle permission denied or error
    });
}

// Call the function to request permission
requestNotificationPermission();

messaging
  .getToken({ vapidKey: 'YOUR_VAPID_PUBLIC_KEY' })
  .then((token) => {
    console.log("Web push token:", token);
    // Send the token to your Django backend to associate it with the user
  })
  .catch((error) => {
    console.log("Error retrieving web push token:", error);
  });


  