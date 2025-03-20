// Define map globally
var map;

$(document).ready(function () {
    var lat = 47.48262506267074;
    var lon = 8.923781163261475;

    // Initialize map globally
    map = L.map('map').setView([lat, lon], 15);

    // Add tile layer (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Add a marker for the farm location
    L.marker([lat, lon]).addTo(map).bindPopup("Farm Location").openPopup();

    // Load terrain status (mock data for now)
    $("#terrain-status").text("Soil moisture: 70% | Temperature: 24°C | Healthy");
});

// Handle Alert Button Click
$("#alert-btn").click(function () {
    // Ensure map is initialized
    if (!map) {
        console.error("Map is not initialized");
        return;
    }

    var latlng = map.getCenter();  // Get the center of the map
    var alertMessage = `🚨 Emergency at (${latlng.lat.toFixed(4)}, ${latlng.lng.toFixed(4)})`;
    
    // Add a red alert marker
    L.marker(latlng, { 
        icon: L.icon({ iconUrl: 'https://img.icons8.com/emoji/48/000000/red-circle-emoji.png', iconSize: [25, 25] }) 
    }).addTo(map).bindPopup("🚨 Alert!");

    // Add alert to the notification card
    $("#notification-list").prepend(`<li>${alertMessage}</li>`);

    // Send the alert to the backend
    $.ajax({
        url: '/send_alert',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            message: alertMessage,
            coordinates: { lat: latlng.lat, lng: latlng.lng }
        }),
        success: function(response) {
            console.log('Alert sent successfully:', response);
        },
        error: function(error) {
            console.error('Error sending alert:', error);
        }
    });
});

// Function to fetch a notification and its solution
function fetchNotification() {
    $.get("/get_notification", function (data) {
        // Display the notification and solution
        var notificationMessage = data.problem;
        var solutionMessage = data.solution;

        // Create a notification list item with a close button
        var notificationItem = `
            <li>
                <h4>🚨 Problem:</h4>
                <p>${notificationMessage}</p>
                <h4>🩹 Solution:</h4>
                <p>${solutionMessage}</p>
                <button class="close-btn">X</button>
            </li>
        `;

        // Prepend the notification item to the list
        $("#notification-list").prepend(notificationItem);
    });
}

// Event listener to remove notification when close button is clicked
$(document).on("click", ".close-btn", function () {
    // Remove the parent <li> of the clicked button (the specific notification)
    $(this).closest('li').remove();
});

// Fetch a notification every 10 seconds
setInterval(fetchNotification, 10000);


