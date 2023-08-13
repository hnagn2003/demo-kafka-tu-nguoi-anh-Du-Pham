// script.js
const imageLog = document.getElementById("imageLog");

// Make a request to the backend
fetch('/')  // Assuming your Express app is running on the same server
    .then(response => response.text())
    .then(log => {
        // Set the received log (which includes image tags) to the log container
        imageLog.innerHTML = log;
    })
    .catch(error => {
        console.error('Error:', error);
    });
