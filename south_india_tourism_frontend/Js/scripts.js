// Mock data
const data = {
    states: [
        {
            name: "Kerala",
            description: "Backwaters, hills, and culture.",
            places: [
                {
                    name: "Munnar",
                    category: "Hill Station",
                    description: "Tea estates and misty mountains.",
                    hotels: [
                        { name: "Sterling Munnar", address: "Chinnakanal Village", amenities: ["wifi", "restaurant", "parking"], distance: 5 },
                        { name: "Taj Munnar", address: "Kallumalai", amenities: ["wifi", "pool", "ac", "restaurant"], distance: 2 }
                    ]
                },
                {
                    name: "Kovalam",
                    category: "Beach",
                    description: "Stunning beaches and resorts.",
                    hotels: [
                        { name: "Kovalam Beach Resort", address: "Kovalam Beach", amenities: ["wifi", "pool", "restaurant"], distance: 1 }
                    ]
                }
            ]
        },
        {
            name: "Tamil Nadu",
            description: "Temples and coastal beauty.",
            places: [
                {
                    name: "Madurai",
                    category: "Cultural",
                    description: "Home to Meenakshi Temple.",
                    hotels: [
                        { name: "Heritage Madurai", address: "Near Meenakshi Temple", amenities: ["wifi", "ac", "restaurant"], distance: 0.5 }
                    ]
                }
            ]
        },
        {
            name: "Karnataka",
            description: "Heritage and modern vibes.",
            places: [
                {
                    name: "Hampi",
                    category: "Historical",
                    description: "Ancient ruins and temples.",
                    hotels: [
                        { name: "Heritage Resort Hampi", address: "Near Virupaksha Temple", amenities: ["wifi", "pool", "restaurant"], distance: 1 }
                    ]
                }
            ]
        },
        {
            name: "Andhra Pradesh",
            description: "Rich history and cuisine.",
            places: [
                {
                    name: "Visakhapatnam",
                    category: "Beach",
                    description: "Scenic beaches and hills.",
                    hotels: [
                        { name: "Novotel Visakhapatnam", address: "Beach Road", amenities: ["wifi", "pool", "ac"], distance: 2 }
                    ]
                }
            ]
        }
    ]
};

// Load state details on state.html (via URL parameter)
function loadStateDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const stateName = urlParams.get('state');
    const state = data.states.find(s => s.name === stateName);
    if (!state) return;
    const stateDiv = document.getElementById('state-details');
    stateDiv.innerHTML = `
        <h2>${state.name}</h2>
        <p>${state.description}</p>
        <h3>Tourist Places</h3>
        <div class="row">
            ${state.places.map(place => `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${place.name}</h5>
                            <p class="card-text">${place.description} (${place.category})</p>
                            <button class="btn btn-secondary" onclick="showHotels('${state.name}', '${place.name}')">View Hotels</button>
                            <button class="btn btn-success" onclick="recommendHotel('${state.name}', '${place.name}')">Recommend Hotel</button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
        <button class="btn btn-secondary mt-3" onclick="window.location.href='index.html'">Back to Map</button>
    `;
}

// Show hotels for a place
function showHotels(stateName, placeName) {
    const state = data.states.find(s => s.name === stateName);
    const place = state.places.find(p => p.name === placeName);
    const stateDiv = document.getElementById('state-details');
    stateDiv.innerHTML = `
        <h2>Hotels in ${place.name}, ${state.name}</h2>
        <div class="mb-3">
            <label for="amenity-filter">Filter by Amenity:</label>
            <select id="amenity-filter" onchange="filterHotels('${state.name}', '${place.name}')">
                <option value="">All</option>
                <option value="wifi">Wi-Fi</option>
                <option value="pool">Pool</option>
                <option value="ac">AC</option>
            </select>
        </div>
        <div class="row" id="hotel-list">
            ${place.hotels.map(hotel => `
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">${hotel.name}</h5>
                            <p class="card-text">${hotel.address}<br>Distance: ${hotel.distance} km<br>Amenities: ${hotel.amenities.join(', ')}</p>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
        <button class="btn btn-secondary mt-3" onclick="loadStateDetails()">Back to ${state.name}</button>
    `;
}

// Filter hotels by amenity
function filterHotels(stateName, placeName) {
    const state = data.states.find(s => s.name === stateName);
    const place = state.places.find(p => p.name === placeName);
    const filter = document.getElementById('amenity-filter').value;
    const hotelList = document.getElementById('hotel-list');
    hotelList.innerHTML = place.hotels
        .filter(hotel => !filter || hotel.amenities.includes(filter))
        .map(hotel => `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${hotel.name}</h5>
                        <p class="card-text">${hotel.address}<br>Distance: ${hotel.distance} km<br>Amenities: ${hotel.amenities.join(', ')}</p>
                    </div>
                </div>
            </div>
        `).join('');
}

// AI-powered hotel recommendation
function recommendHotel(stateName, placeName) {
    const state = data.states.find(s => s.name === stateName);
    const place = state.places.find(p => p.name === placeName);
    const preferences = prompt("Enter preferred amenities (e.g., wifi,pool):")?.split(',').map(s => s.trim()) || [];
    if (preferences.length === 0) return alert("Please enter some preferences!");
    const scores = place.hotels.map(hotel => ({
        hotel,
        score: preferences.reduce((sum, pref) => sum + (hotel.amenities.includes(pref) ? 1 : 0), 0)
    }));
    const best = scores.sort((a, b) => b.score - a.score)[0];
    if (best.score === 0) {
        alert("No hotels match your preferences.");
    } else {
        alert(`Recommended: ${best.hotel.name} (${best.score}/${preferences.length} preferences matched)`);
    }
}

// Admin: Simulate adding a hotel
// function addHotel() {
//     const name = document.getElementById('hotelName').value;
//     const placeName = document.getElementById('placeName').value;
//     const address = document.getElementById('address').value;
//     const amenities = document.getElementById('amenities').value.split(',').map(s => s.trim());
//     const distance = parseFloat(document.getElementById('distance').value);
//     if (!name || !placeName || !address || !amenities.length || isNaN(distance)) {
//         alert("Please fill all fields!");
//         return;
//     }
//     alert(`Hotel Added (Simulation):\nName: ${name}\nPlace: ${placeName}\nAddress: ${address}\nAmenities: ${amenities.join(', ')}\nDistance: ${distance} km`);
//     document.getElementById('adminModal').querySelector('.btn-close').click();
// }

// Load state details on page load for state.html
if (window.location.pathname.includes('state.html')) {
    window.onload = loadStateDetails;
}