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

// Initialize notification count
let notificationCount = 0;

function fetchNotification() {
    $.get("/get_notification", function(data) {
        var notificationMessage = data.problem;
        var solutionMessage = data.solution;

        // Create a notification item for the list
        var notificationItem = `
            <li>
                <div class="card mb-2">
                    <div class="card-body">
                        <h6 class="card-title">🚨 Alert</h6>
                        <p>${notificationMessage}</p>
                        <h6 class="card-subtitle mb-2">🩹 Solution:</h6>
                        <p>${solutionMessage}</p>
                        <button class="close-btn btn btn-danger btn-md">X</button>
                    </div>
                </div>
            </li>
        `;

        // Prepend notification item to the list
        $("#notification-list").prepend(notificationItem);

        // Create a new toast element
        var toast = `
            <div class="toast align-items-center text-bg-warning border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <strong>🚨 Alert:</strong> ${notificationMessage}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        `;

        // Append the toast to the container
        $("#toast-container").append(toast);

        // Initialize and show the toast
        var toastElement = $(".toast").last()[0];
        var bootstrapToast = new bootstrap.Toast(toastElement);
        bootstrapToast.show();

        // Update notification count
        notificationCount++;
        
        // Update badge number on the bell icon
        const badge = $('#notification-badge');
        badge.text(notificationCount);

        // Show the badge if there are notifications, otherwise hide it
        if (notificationCount > 0) {
            badge.show();
        } else {
            badge.hide();
        }
    });
}



// Event listener to remove notification when close button is clicked
$(document).on("click", ".close-btn", function () {
    $(this).closest('li').remove();

    // Update notification count
    notificationCount--;
        
    // Update badge number on the bell icon
    const badge = $('#notification-badge');
    badge.text(notificationCount);

    // Show the badge if there are notifications, otherwise hide it
    if (notificationCount > 0) {
        badge.show();
    } else {
        badge.hide();
    }
});

// Fetch a notification every 10 seconds
setInterval(fetchNotification, 5000);





document.getElementById('alert-btn').addEventListener('click', function () {
    const alertType = document.getElementById('alert-type').value;
    const alertMessage = document.getElementById('alert-message').value;

    // Show the alert modal
    const alertModal = new bootstrap.Modal(document.getElementById('alertModal'));
    alertModal.show();
});



document.getElementById('clear-notifications-btn').addEventListener('click', function () {
    const notificationList = document.getElementById('notification-list');
    notificationList.innerHTML = ''; // Clear all notifications

    // Reset the notification count
    notificationCount = 0;

    // Update the badge
    const badge = $('#notification-badge');
    badge.text(notificationCount);
    badge.hide(); // Hide the badge when there are no notifications
});

// Function to fetch the status of the terrain
function fetchStatus() {
    $.get("/get_status", function(data) {
        
        // Extract data from the response or provide default values
        var temperature = data["Temperature_15Min"] + " °C";
        var wind_speed = data["WindSpeed_15Min"] + " m/s";
        var humidity = data["HumidityRel_15Min"] + " %";
        var air_pressure = data["Airpressure_15Min"] + " hPa";

        // Update the terrain status in the card
        $("#temperature").text(temperature);
        $("#wind-speed").text(wind_speed);
        $("#humidity").text(humidity);
        $("#air-pressure").text(air_pressure);

    });
}

setInterval(fetchStatus, 1000);

