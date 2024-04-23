document.addEventListener("DOMContentLoaded", function() {
    var map = initializeMap();  // Call to initialize the map

    window.updateMapAndStatistics = function() {
        var routeId = document.getElementById('routeSelect').value;
        clearMap(map);

        if (routeId) {
            fetchStopsAndRoute(map, routeId);
            fetchRouteStatistics(routeId);
        } else {
            resetStatistics();
        }
    };
});

function initializeMap() {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    return map;
}

function fetchStopsAndRoute(map, routeId) {
    // Fetch and display stops and route polyline for selected route
    // Implement fetching logic here
}

function fetchRouteStatistics(routeId) {
    // Fetch and display statistics for selected route
    // Implement fetching logic here
}

function resetStatistics() {
    // Reset statistics display when no route is selected
    // Implement reset logic here
}

function clearMap(map) {
    map.eachLayer(function(layer) {
        if (!(layer instanceof L.TileLayer)) {
            map.removeLayer(layer);
        }
    });
}
