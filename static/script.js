// Define map globally
var map;

$(document).ready(function () {
    var lat = 47.48262506267074;
    var lon = 8.923781163261475;

    // Initialize map globally
    map = L.map('map').setView([lat, lon], 15);

    // Add satellite tile layer (Esri)
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    }).addTo(map);

    // Add a marker for the farm location
    L.marker([lat, lon]).addTo(map).bindPopup("Amir Location").openPopup();

    // Load terrain status (mock data for now)
    $("#terrain-status").text("Soil moisture: 70% | Temperature: 24°C | Healthy");
});


// Function to fetch a notification and its solution
function fetchNotification() {
    $.get("/get_notification", function(data) {
        var notificationMessage = data.problem;
        var solutionMessage = data.solution;

        var notificationItem = `
            <li>
                <div class="card mb-2">
                    <div class="card-body">
                        <h6 class="card-title">🚨 Alert</h5>
                        <p>${notificationMessage}</p>
                        <h6 class="card-subtitle mb-2">🩹 Solution:</h6>
                        <p>${solutionMessage}</p>
                        <button class="close-btn btn btn-danger btn-md">X</button>
                    </div>
                </div>
            </li>
        `;

        $("#notification-list").prepend(notificationItem);
    });
}

// Event listener to remove notification when close button is clicked
$(document).on("click", ".close-btn", function () {
    $(this).closest('li').remove();
});

// Fetch a notification every 10 seconds
setInterval(fetchNotification, 10000);





document.getElementById('send-alert-btn').addEventListener('click', function () {
    const alertType = document.getElementById('alert-type').value;
    const alertMessage = document.getElementById('alert-message').value;

    // Log the alert data
    console.log('Alert Type:', alertType);
    console.log('Alert Message:', alertMessage);

    // Send the alert data to the backend
    $.ajax({
        url: '/send_alert', // Replace with your backend endpoint
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            type: alertType,
            message: alertMessage
        }),
        success: function (response) {
            console.log('Alert sent successfully:', response);

            // Optionally, show a success message to the user
            alert('Alert sent successfully!');
        },
        error: function (error) {
            console.error('Error sending alert:', error);

            // Optionally, show an error message to the user
            alert('Failed to send alert. Please try again.');
        }
    });

    // Close the modal
    const alertModal = bootstrap.Modal.getInstance(document.getElementById('alertModal'));
    alertModal.hide();
});



document.getElementById('clear-notifications-btn').addEventListener('click', function () {
    const notificationList = document.getElementById('notification-list');
    notificationList.innerHTML = ''; // Clear all notifications
});

// Function to fetch the status of the terrain
function fetchStatus() {
    $.get("/get_status", function(data) {
        // Extract data from the response or provide default values
        var soilMoisture = data.soil_moisture !== undefined ? `${data.soil_moisture}%` : "Data unavailable";
        var temperature = data.temperature !== undefined ? `${data.temperature}°C` : "Data unavailable";
        var healthStatus = data.health_status !== undefined ? data.health_status : "Data unavailable";

        // Update the terrain status in the card
        $("#soil-moisture").text(soilMoisture);
        $("#temperature").text(temperature);
        $("#health-status").text(healthStatus);
    });
}

setInterval(fetchStatus, 1000);

