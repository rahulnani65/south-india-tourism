// static/core/js/karnataka.js

'use strict';

// --- GLOBAL FUNCTIONS (Accessible from HTML onclick) ---

// Global variables for the map modal
// --- GOOGLE MAP MODAL LOGIC (DEFINITIVE FIX for Accessibility & Focus) ---

// Global variables to hold map state
let mapModalInstance = null;
let modalMap = null;
let modalMarker = null;

// This is a temporary variable to pass data to the event listener
let pendingMapData = null;

// 1. A simple function called by HTML's onclick.
// Its ONLY job is to store the data and show the modal.
window.showPlaceOnMap = function(latitude, longitude, placeName) {
    // Store the data for the map we want to show
    pendingMapData = { lat: parseFloat(latitude), lng: parseFloat(longitude), name: placeName };

    // Initialize the Bootstrap modal instance if it doesn't exist
    if (!mapModalInstance) {
        const modalEl = document.getElementById('mapModal');
        if (!modalEl) {
            console.error('Modal with ID "mapModal" not found!');
            return;
        }
        mapModalInstance = new bootstrap.Modal(modalEl);
    }
    
    // Show the modal. The 'shown.bs.modal' event will handle the rest.
    mapModalInstance.show();
};

// 2. The main logic runs ONLY AFTER the modal is fully visible.
document.addEventListener('DOMContentLoaded', function() {
    const mapModalEl = document.getElementById('mapModal');
    if (mapModalEl) {
        mapModalEl.addEventListener('shown.bs.modal', function () {
            // Check if there's a map to be loaded
            if (!pendingMapData) return;

            const position = pendingMapData;
            const modalTitle = document.getElementById('mapModalLabel');
            if (modalTitle) modalTitle.textContent = position.name;

            // Initialize the Google Map object if it's the first time
            if (!modalMap) {
                modalMap = new google.maps.Map(document.getElementById('modalMapContainer'), {
                    center: position,
                    zoom: 15,
                    mapTypeControl: true,
                    streetViewControl: true,
                    fullscreenControl: true
                });
            } else {
                // If map already exists, just update its center.
                modalMap.setCenter(position);
            }
            
            // This is a good practice to ensure the map renders correctly after the modal resize.
            google.maps.event.trigger(modalMap, 'resize');
            modalMap.setCenter(position);

            // Update the marker.
            if (modalMarker) modalMarker.setMap(null); // Clear previous marker
            
            modalMarker = new google.maps.Marker({
                position: position,
                map: modalMap,
                title: position.name,
                animation: google.maps.Animation.DROP
            });

            // Clean up the temporary data
            pendingMapData = null;
        });
    }
});

// Other globally accessible functions
window.fetchGeminiRecommendations = function() {
    const placeSelect = document.getElementById("user-place");
    const recommendationsDiv = document.getElementById("gemini-recommended-places");
    if (!placeSelect || !recommendationsDiv) return;

    const selectedOption = placeSelect.options[placeSelect.selectedIndex];
    const lat = selectedOption.getAttribute('data-lat'), lon = selectedOption.getAttribute('data-lng');
    if (!lat || !lon) {
        alert("Please select your current location for personalized recommendations.");
        return;
    }
    recommendationsDiv.innerHTML = `<div class="recommendation-loading"><div class="spinner-border text-success" role="status"></div><h5 class="mt-3">Finding perfect places for you...</h5></div>`;
    
    const params = new URLSearchParams({
        latitude: lat,
        longitude: lon,
        user_place: selectedOption.value,
        place_type: document.getElementById("gemini-place-type").value,
        budget: document.getElementById("budget").value,
        duration: document.getElementById("duration").value,
        enhanced: 'true',
        context: 'karnataka'
    });

    const geminiApiUrl = window.GEMINI_RECOMMENDATIONS_URL || "/state/get-gemini-recommendations/";
    fetch(`${geminiApiUrl}?${params.toString()}`)
      .then(res => res.ok ? res.json() : Promise.reject(new Error(`Network error: ${res.statusText}`)))
      .then(data => { if (data.error) throw new Error(data.error); renderRecommendations(data); })
      .catch(err => {
          console.error('Error fetching recommendations:', err);
          recommendationsDiv.innerHTML = `<div class="alert alert-danger m-3">Sorry, we couldn't fetch recommendations. Error: ${err.message}</div>`;
      });
};

window.clearRecommendations = function() {
    const div = document.getElementById("gemini-recommended-places");
    if (div) div.innerHTML = `<div class="recommendation-placeholder text-center"><i class="fas fa-compass fa-3x text-muted mb-3"></i><h5>Ready to Discover?</h5><p>Select your preferences above and get recommendations for Karnataka.</p></div>`;
};

window.generateItinerary = function() {
    const input = document.getElementById('startingPoint');
    if (input.value === "") input.value = "Bengaluru";

    const container = document.getElementById('itineraryDays');
    const display = document.getElementById('generatedItinerary');
    if (!container || !display) return;

    display.classList.remove('d-none');
    container.innerHTML = `<div class="itinerary-loading-container"><div class="spinner-border text-success"></div><h5 class="loading-title mt-3">Crafting your Karnataka itinerary...</h5></div>`;

    setTimeout(() => {
        const places = window.PLACES_WITH_WEATHER || [];
        const plan = createSmartItinerary(parseInt(document.getElementById('tripDuration').value), document.getElementById('travelStyle').value, places);
        displayItinerary(plan, input.value, container);
    }, 1200);
};

window.resetItinerary = function() {
    document.getElementById('itineraryForm').reset();
    document.getElementById('generatedItinerary').classList.add('d-none');
    document.getElementById('itineraryDays').innerHTML = '';
};

window.saveItinerary = () => {
    const toastEl = document.getElementById('itineraryToast');
    if (toastEl && window.bootstrap) new bootstrap.Toast(toastEl).show();
};

window.exportItinerary = () => alert('Export functionality is a work in progress!');


// --- CODE THAT RUNS AFTER THE PAGE LOADS ---

document.addEventListener('DOMContentLoaded', function() {
    initializePage();

    // Helper functions that don't need to be global
    function initializePage() {
        initializeAOS();
        initializeNavbarScroll();
        initializeBackToTopButton();
        initializeCategoryFilter();
        initializeCalendar();
        initializeItineraryPlanner();
    }

    function initializeAOS() { if (typeof AOS !== 'undefined') AOS.init({ duration: 800, once: true, offset: 50 }); }
    function initializeNavbarScroll() {
        const navbar = document.querySelector('.navbar.sticky-top'), secondaryNav = document.querySelector('.secondary-nav');
        if (!navbar || !secondaryNav) return;
        window.addEventListener('scroll', () => { const isScrolled = window.scrollY > 150; navbar.style.display = isScrolled ? 'none' : ''; secondaryNav.classList.toggle('active', isScrolled); }, { passive: true });
    }
    function initializeBackToTopButton() {
        const btn = document.querySelector('.back-to-top'); if (!btn) return;
        window.addEventListener('scroll', () => { btn.classList.toggle('show', window.pageYOffset > 300); }, { passive: true });
        btn.addEventListener('click', e => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
    }
    function initializeCategoryFilter() {
        const filter = document.getElementById('categoryFilter'); if (!filter) return;
        filter.addEventListener('change', filterPlacesByCategory);
        filterPlacesByCategory(); // Initial run
    }
    function filterPlacesByCategory() {
        const category = document.getElementById('categoryFilter').value;
        const cards = document.querySelectorAll('.place-card-wrapper'); let count = 0;
        cards.forEach(card => {
            const cardCat = card.dataset.category || 'all';
            const show = (category === 'all' || cardCat.includes(category));
            card.style.display = show ? 'block' : 'none';
            if (show) count++;
        });
        const countEl = document.getElementById('place-count'); if(countEl) countEl.innerHTML = `<small>Showing ${count} of ${cards.length} places</small>`;
    }
    
    function initializeCalendar() {
        const eventsContainer = document.getElementById('events-list');
        if (!eventsContainer) return;
        const events = [
            { date: new Date(new Date().getFullYear(), 9, 3), title: 'Mysuru Dasara', place: 'Mysore', description: 'A spectacular 10-day festival culminating in a grand procession with decorated elephants.' },
            { date: new Date(new Date().getFullYear() + 1, 0, 14), title: 'Makar Sankranti', place: 'Throughout Karnataka', description: 'A harvest festival celebrated with kite flying, and exchanging sweets made of sesame and jaggery.' },
            { date: new Date(new Date().getFullYear() + 1, 2, 29), title: 'Ugadi', place: 'Throughout Karnataka', description: 'The Kannada New Year, celebrated with special dishes like Bevu Bella, symbolizing life\'s different facets.' },
            { date: new Date(new Date().getFullYear(), 10, 1), title: 'Hampi Utsav', place: 'Hampi', description: 'A grand cultural extravaganza celebrating the heritage of the Vijayanagara empire amidst the ruins of Hampi.' },
            { date: new Date(new Date().getFullYear(), 10, 15), title: 'Kambala Festival', place: 'Coastal Karnataka', description: 'An exciting traditional buffalo race held in the paddy fields of coastal regions.' }
        ];
        if (events.length === 0) return;
        eventsContainer.innerHTML = events.map(event =>
            `<div class="col-md-6 col-lg-4"><div class="card event-card h-100"><div class="card-body"><h5 class="card-title">${event.title}</h5><p class="card-text"><i class="fas fa-calendar-alt me-2"></i>${event.date.toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}</p><p class="card-text"><i class="fas fa-map-marker-alt me-2"></i>${event.place}</p><p class="card-text text-muted">${event.description}</p></div></div></div>`
        ).join('');
    }
    
    function initializeItineraryPlanner() {
        const genBtn = document.getElementById('generate-itinerary-btn');
        if (genBtn) genBtn.addEventListener('click', window.generateItinerary);
    }
});

// Helper functions for itinerary generation (can be inside or outside DOMContentLoaded)
function createSmartItinerary(duration, style, places) {
    const keywords = { adventure: ['park', 'hills', 'wildlife', 'lake', 'dam', 'adventure', 'falls', 'beach'], cultural: ['temple', 'fort', 'historical', 'museum', 'monument', 'city', 'cultural', 'palace'], relaxation: ['lake', 'park', 'garden', 'resort', 'hills', 'relaxation', 'beach'] };
    let filtered = places.filter(p => (keywords[style] || []).some(k => p.category.includes(k) || p.name.toLowerCase().includes(k)));
    if (filtered.length < duration * 2) filtered = [...places];
    const shuffled = [...filtered].sort(() => 0.5 - Math.random());
    const plan = []; let index = 0;
    for (let day = 1; day <= duration; day++) {
      const perDay = Math.ceil(shuffled.length / duration) || 2;
      const dayPlaces = shuffled.slice(index, index + perDay);
      if (dayPlaces.length > 0) plan.push({ day, places: dayPlaces });
      index += perDay;
    }
    return plan;
}

function displayItinerary(plan, start, container) {
    if (!plan || plan.length === 0) { container.innerHTML = '<p class="text-danger">Could not generate an itinerary. Please try again.</p>'; return; }
    let html = `<p class="text-muted">Starting from: <strong>${start}</strong></p>`;
    html += plan.map(d => `<div class="itinerary-day"><h6><i class="fas fa-calendar-day"></i> Day ${d.day}</h6>${d.places.map((p, i) => {
      const time = i === 0 ? "Morning" : (i === 1 ? "Afternoon" : "Evening");
      const name = p.name.replace(/'/g, "\\'");
      return `<div class="itinerary-place"><span class="place-time">${time}</span><div class="place-details"><strong>${p.name}</strong><small class="d-block text-muted">${p.category.charAt(0).toUpperCase() + p.category.slice(1)}</small></div><button class="btn btn-sm btn-outline-primary" onclick="showPlaceOnMap('${p.latitude}', '${p.longitude}', '${name}')" title="Show on Map"><i class="fas fa-map-marker-alt"></i></button></div>`;
    }).join('')}</div>`).join('');
    container.innerHTML = html;
}

function renderRecommendations(data) {
    const div = document.getElementById("gemini-recommended-places"), places = data.gemini_recommended_places;
    if (!places || places.length === 0) { div.innerHTML = `<div class="alert alert-info m-3">No recommendations found. Please try different filters.</div>`; return; }
    let html = '<div class="row p-3">';
    places.forEach(place => {
      const name = place.name.replace(/'/g, "\\'").replace(/"/g, '"');
      html += `<div class="col-md-6 mb-4"><div class="card recommendation-card h-100"><div class="card-body d-flex flex-column"><h5 class="card-title">${place.name}</h5><span class="recommendation-badge mb-2"><i class="fas fa-star"></i> Rating: ${place.rating || 'N/A'}</span><p class="reasoning"><em>"${place.reasoning}"</em></p><div class="mt-auto pt-2"><button class="btn btn-primary w-100" onclick="showPlaceOnMap('${place.latitude}', '${place.longitude}', '${name}')"><i class="fas fa-map-marker-alt"></i> View on Map</button></div></div></div></div>`;
    });
    div.innerHTML = html + '</div>';
}