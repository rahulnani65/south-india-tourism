// static/core/js/karnataka.js
// This file contains all the client-side JavaScript logic for the enhanced Karnataka state page.

document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  // --- GLOBAL/MODULE-LEVEL VARIABLES ---
  const geminiApiUrl = "/state/get-gemini-recommendations/"; // Using static path as Django template tags are not available here.
  let mapModalInstance = null;
  let modalMap = null;
  let modalMarker = null;

  // --- PRIMARY INITIALIZATION ---
  function initializePage() {
    initializeAOS();
    initializeNavbarScroll();
    initializeBackToTopButton();
    initializeCategoryFilter();
    initializeCalendar();
    // Functions called from HTML via onclick don't need to be in an initializer
  }

  // --- UI & UX INITIALIZERS ---

  function initializeAOS() {
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 800,
        once: true,
        offset: 50,
      });
    }
  }

  function initializeNavbarScroll() {
    const navbar = document.querySelector('.navbar.sticky-top');
    const secondaryNav = document.querySelector('.secondary-nav');
    if (!navbar || !secondaryNav) return;

    window.addEventListener('scroll', () => {
      const isScrolled = window.scrollY > 150;
      navbar.style.display = isScrolled ? 'none' : '';
      secondaryNav.classList.toggle('active', isScrolled);
    }, { passive: true });
  }

  function initializeBackToTopButton() {
    const backToTopButton = document.querySelector('.back-to-top');
    if (!backToTopButton) return;

    window.addEventListener('scroll', () => {
      backToTopButton.classList.toggle('show', window.pageYOffset > 300);
    }, { passive: true });

    backToTopButton.addEventListener('click', e => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- PLACES & FILTERING LOGIC ---

  function initializeCategoryFilter() {
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
      filterPlacesByCategory(); // Initial filter on page load
      categoryFilter.addEventListener('change', filterPlacesByCategory);
    }
  }

  function filterPlacesByCategory() {
    const selectedCategory = document.getElementById('categoryFilter').value;
    const placeCards = document.querySelectorAll('.place-card-wrapper');
    let visibleCount = 0;

    placeCards.forEach(card => {
      const cardCategory = card.dataset.category || 'all';
      const shouldShow = (selectedCategory === 'all' || cardCategory.includes(selectedCategory));
      
      card.style.display = shouldShow ? 'block' : 'none';
      if (shouldShow) {
        visibleCount++;
      }
    });
    updatePlaceCount(visibleCount, placeCards.length);
  }

  function updatePlaceCount(visible, total) {
    const countDisplay = document.getElementById('place-count');
    if (countDisplay) {
      countDisplay.innerHTML = `<small>Showing ${visible} of ${total} places</small>`;
    }
  }
  
  // --- GOOGLE MAP MODAL LOGIC ---

  function initializeMapModal() {
    const mapModalEl = document.getElementById('mapModal');
    if (mapModalEl) {
      mapModalInstance = new bootstrap.Modal(mapModalEl);
      
      mapModalEl.addEventListener('shown.bs.modal', function () {
        if (modalMap) {
            google.maps.event.trigger(modalMap, 'resize');
            if (modalMarker) {
                modalMap.setCenter(modalMarker.getPosition());
            }
        }
      });
    }
  }

  // This function is exposed to the global scope to be called by onclick attributes in the HTML
  window.showPlaceOnMap = function(lat, lng, name) {
    const mapModal = new bootstrap.Modal(document.getElementById('mapModal'));
    mapModal.show();
    if (!modalMap) {
      modalMap = new google.maps.Map(document.getElementById('modalMapContainer'), {
        center: { lat: parseFloat(lat), lng: parseFloat(lng) },
        zoom: 15,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true
      });
    } else {
      modalMap.setCenter({ lat: parseFloat(lat), lng: parseFloat(lng) });
    }
    if (modalMarker) {
      modalMarker.setMap(null);
    }
    modalMarker = new google.maps.Marker({
      position: { lat: parseFloat(lat), lng: parseFloat(lng) },
      map: modalMap,
      title: name,
      animation: google.maps.Animation.DROP
    });
    const infoWindow = new google.maps.InfoWindow({
      content: `<div class="p-2"><h6>${name}</h6><p>Latitude: ${lat}<br>Longitude: ${lng}</p></div>`
    });
    modalMarker.addListener('click', () => {
      infoWindow.open(modalMap, modalMarker);
    });
    infoWindow.open(modalMap, modalMarker);
  };

  // --- EVENTS CALENDAR LOGIC ---

  function initializeCalendar() {
    const events = [
      { date: new Date('2025-03-29'), title: 'Ugadi', place: 'Throughout Karnataka', description: 'Kannada New Year celebrated with traditional foods and rituals.' },
      { date: new Date('2025-04-05'), title: 'Karaga Festival', place: 'Bengaluru', description: 'A centuries-old festival dedicated to Draupadi, celebrated with a grand procession.' },
      { date: new Date('2025-10-12'), title: 'Mysore Dasara', place: 'Mysore', description: 'Ten-day royal festival with processions, cultural events, and illuminated palaces.' },
      { date: new Date('2025-03-30'), title: 'Vairamudi Festival', place: 'Melukote', description: 'Religious festival where the deity is adorned with a diamond-studded crown.' },
      { date: new Date('2025-11-15'), title: 'Kambala', place: 'Coastal Karnataka', description: 'Traditional buffalo race held in the waterlogged fields of coastal Karnataka.' },
      { date: new Date('2025-11-12'), title: 'Deepavali', place: 'Throughout Karnataka', description: 'Festival of lights celebrated with fireworks and sweets.' }
    ];

    let currentDate = new Date();
    let selectedDate = null;
    
    const elements = {
      grid: document.getElementById('calendarGrid'),
      monthYear: document.getElementById('calendarMonthYear'),
      eventList: document.getElementById('eventList'),
      prevBtn: document.getElementById('calendarPrev'),
      nextBtn: document.getElementById('calendarNext'),
      prompt: document.getElementById('eventPrompt')
    };

    if (!elements.grid || !elements.monthYear || !elements.eventList) return;

    function renderCalendar() {
      const month = currentDate.getMonth();
      const year = currentDate.getFullYear();
      elements.monthYear.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;
      
      elements.grid.innerHTML = '';
      const firstDayOfMonth = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const today = new Date();

      for (let i = 0; i < firstDayOfMonth; i++) {
        elements.grid.insertAdjacentHTML('beforeend', '<div class="calendar-cell"></div>');
      }

      for (let d = 1; d <= daysInMonth; d++) {
        const cellDate = new Date(year, month, d);
        let classes = 'calendar-cell';
        const hasEvent = events.some(ev => ev.date.toDateString() === cellDate.toDateString());
        if (hasEvent) classes += ' event-day';
        if (cellDate.toDateString() === today.toDateString()) classes += ' today';
        if (selectedDate && cellDate.toDateString() === selectedDate.toDateString()) classes += ' selected';
        
        elements.grid.insertAdjacentHTML('beforeend', `<div class="${classes}" data-date="${cellDate.toISOString()}">${d}${hasEvent ? ' <span style="color:#007bff;">•</span>' : ''}</div>`);
      }
    }

    function renderEvents(date) {
        let html = '';
        const filteredEvents = events.filter(ev => ev.date.toDateString() === date.toDateString());
        
        if (filteredEvents.length === 0) {
            html = '<div class="event-item"><p>No scheduled events for this day.</p></div>';
        } else {
            html = filteredEvents.map(ev => `
              <div class="event-item">
                <h4>${ev.title} <span class="event-date">(${ev.date.toLocaleDateString()})</span></h4>
                <p><strong>Location:</strong> ${ev.place}</p>
                <p>${ev.description}</p>
              </div>`
            ).join('');
        }
        elements.eventList.innerHTML = html;
    }

    elements.grid.addEventListener('click', e => {
      if (e.target.matches('.calendar-cell[data-date]')) {
        selectedDate = new Date(e.target.dataset.date);
        renderCalendar();
        renderEvents(selectedDate);
      }
    });

    function changeMonth(offset) {
      currentDate.setMonth(currentDate.getMonth() + offset);
      selectedDate = null;
      renderCalendar();
      if(elements.prompt) elements.eventList.innerHTML = elements.prompt.outerHTML;
    }

    elements.prevBtn.addEventListener('click', () => changeMonth(-1));
    elements.nextBtn.addEventListener('click', () => changeMonth(1));

    renderCalendar();
  }
  
  // --- AI RECOMMENDATIONS LOGIC ---

  // Exposed to window for onclick attribute in HTML
  window.fetchGeminiRecommendations = function() {
    const placeSelect = document.getElementById("user-place");
    const recommendationsDiv = document.getElementById("gemini-recommended-places");
    
    if (!placeSelect || !recommendationsDiv) return;

    const selectedOption = placeSelect.options[placeSelect.selectedIndex];
    const latitude = selectedOption.getAttribute('data-lat');
    const longitude = selectedOption.getAttribute('data-lng');
    const placeType = document.getElementById("gemini-place-type").value;
    const budget = document.getElementById("budget").value;
    const duration = document.getElementById("duration").value;

    if (!latitude || !longitude) {
      alert("Please select your current location to get personalized recommendations.");
      return;
    }

    recommendationsDiv.innerHTML = `<div class="recommendation-loading"><div class="spinner-border text-success" role="status"></div><h5 class="mt-3">Analyzing your preferences...</h5></div>`;

    const params = new URLSearchParams({
        latitude,
        longitude,
        user_place: selectedOption.value,
        place_type: placeType,
        budget,
        duration,
        enhanced: 'true',
        context: 'karnataka' // CRITICAL: This provides context to the AI
    });

    fetch(`${geminiApiUrl}?${params.toString()}`)
      .then(response => {
          if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
          return response.json();
      })
      .then(data => {
        if (data.error) throw new Error(data.error);
        renderRecommendations(data);
      })
      .catch(error => {
        console.error('Error fetching recommendations:', error);
        recommendationsDiv.innerHTML = `<div class="alert alert-danger m-3">Sorry, we couldn't fetch recommendations at this time. Error: ${error.message}</div>`;
      });
  };

  function renderRecommendations(data) {
    const recommendationsDiv = document.getElementById("gemini-recommended-places");
    const places = data.gemini_recommended_places;
    const weatherData = data.weather_data;

    if (!places || places.length === 0) {
        recommendationsDiv.innerHTML = `<div class="alert alert-info m-3">No recommendations found. Please try different filters.</div>`;
        return;
    }

    let html = '';

    if (weatherData) {
        html += `
        <div class="recommendation-weather m-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title"><i class="fas fa-cloud-sun"></i> Current Weather in the area</h5>
                    <div class="row">
                        <div class="col-md-3"><p class="mb-0"><strong>Temperature:</strong> ${weatherData.temperature}°C</p></div>
                        <div class="col-md-3"><p class="mb-0"><strong>Weather:</strong> ${weatherData.weather}</p></div>
                        <div class="col-md-3"><p class="mb-0"><strong>Humidity:</strong> ${weatherData.humidity}%</p></div>
                        <div class="col-md-3"><p class="mb-0"><strong>Description:</strong> ${weatherData.description}</p></div>
                    </div>
                </div>
            </div>
        </div>`;
    }

    html += '<div class="row p-3">';
    places.forEach(place => {
      const escapedName = place.name.replace(/'/g, "\\'").replace(/"/g, '"');
      const rating = place.rating || 'N/A';
      const reasoning = place.reasoning || 'No description available';
      
      html += `
        <div class="col-md-6 mb-4">
          <div class="card recommendation-card h-100">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title">${place.name}</h5>
                <span class="recommendation-badge">
                    <i class="fas fa-star"></i> Rating: ${rating}
                </span>
                
                ${weatherData ? `
                <div class="recommendation-weather my-3 p-2">
                    <h6><i class="fas fa-cloud"></i> Weather</h6>
                    <p class="mb-1"><small><i class="fas fa-temperature-high"></i> ${weatherData.temperature}°C, ${weatherData.weather}</small></p>
                </div>
                ` : ''}

                <p class="location-info">
                    <i class="fas fa-map-marker-alt"></i> 
                    ${parseFloat(place.latitude).toFixed(4)}, ${parseFloat(place.longitude).toFixed(4)}
                </p>
                <p class="reasoning">${reasoning}</p>
                <div class="recommendation-actions mt-auto">
                    <button class="btn btn-primary" onclick="showPlaceOnMap('${place.latitude}', '${place.longitude}', '${escapedName}')">
                        <i class="fas fa-map-marker-alt"></i> Show on Map
                    </button>
                    <button class="btn btn-outline-secondary" onclick="addToFavorites('${escapedName}', ${place.latitude}, ${place.longitude}, event)">
                        <i class="far fa-heart"></i> Save
                    </button>
                </div>
            </div>
          </div>
        </div>
      `;
    });
    html += '</div>';
    recommendationsDiv.innerHTML = html;
  }

  // Exposed to window for onclick attribute in HTML
  window.clearRecommendations = function() {
    const recommendationsDiv = document.getElementById("gemini-recommended-places");
    if(recommendationsDiv) {
        recommendationsDiv.innerHTML = `<div class="recommendation-placeholder text-center"><i class="fas fa-compass fa-3x text-muted mb-3"></i><h5>Ready to Discover?</h5><p>Select your preferences above and get personalized recommendations.</p></div>`;
    }
  };

  // --- Review System ---
  let selectedRating = 0;
  const stars = document.querySelectorAll('.star-rating');
  stars.forEach(star => {
    star.addEventListener('click', function() {
      const rating = parseInt(this.dataset.rating);
      selectedRating = rating;
      stars.forEach((s, index) => {
        if (index < rating) s.classList.add('active');
        else s.classList.remove('active');
      });
    });
    star.addEventListener('mouseenter', function() {
      const rating = parseInt(this.dataset.rating);
      stars.forEach((s, index) => {
        if (index < rating) s.style.color = '#ffd700';
      });
    });
    star.addEventListener('mouseleave', function() {
      stars.forEach((s, index) => {
        if (index < selectedRating) s.style.color = '#ffd700';
        else s.style.color = '#dee2e6';
      });
    });
  });
  const addReviewForm = document.getElementById('addReviewForm');
  if (addReviewForm) {
    addReviewForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const placeId = document.getElementById('reviewPlace').value;
      const comment = document.getElementById('reviewComment').value;
      if (!placeId || !comment || selectedRating === 0) {
        alert('Please fill in all fields and select a rating');
        return;
      }
      submitReview(placeId, selectedRating, comment);
    });
  }
  function submitReview(placeId, rating, comment) {
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
      alert('CSRF token not found. Please refresh the page and try again.');
      return;
    }
    fetch(window.ADD_REVIEW_URL.replace('0', placeId), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: `rating=${rating}&comment=${encodeURIComponent(comment)}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Review submitted!');
        window.location.reload();
        return;
      } else {
        alert('Error submitting review: ' + (data.error || 'Unknown error'));
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error submitting review: ' + error.message);
    });
  }
  window.filterReviews = function(alwaysShowNew) {
    const ratingFilter = document.getElementById('reviewFilter').value;
    const placeFilter = document.getElementById('placeFilter').value;
    const reviewCards = document.querySelectorAll('.review-card');
    let visibleCount = 0;
    reviewCards.forEach(card => {
      const rating = parseInt(card.dataset.rating);
      const place = String(card.dataset.place);
      let showCard = true;
      if (alwaysShowNew && card.hasAttribute('data-newly-added')) {
        card.style.display = 'block';
        visibleCount++;
        return;
      }
      if (ratingFilter !== 'all') {
        const minRating = parseInt(ratingFilter);
        if (rating < minRating) showCard = false;
      }
      if (placeFilter !== 'all' && place !== String(placeFilter)) showCard = false;
      card.style.display = showCard ? 'block' : 'none';
      if (showCard) visibleCount++;
    });
    let noMsg = document.getElementById('no-reviews-message');
    if (visibleCount === 0) {
      if (!noMsg) {
        noMsg = document.createElement('div');
        noMsg.id = 'no-reviews-message';
        noMsg.className = 'text-center py-4';
        noMsg.innerHTML = `
          <i class="fas fa-comment-slash fa-3x text-muted mb-3"></i>
          <p class="text-muted">No reviews found for the selected filter.</p>
        `;
        document.getElementById('reviewsContainer').appendChild(noMsg);
      }
    } else {
      if (noMsg) noMsg.remove();
    }
  };

  // --- Itinerary Builder Logic (copied and adapted from tamil_nadu.js) ---
  window.generateItinerary = function() {
    const duration = parseInt(document.getElementById('tripDuration').value);
    const style = document.getElementById('travelStyle').value;
    const startingPoint = document.getElementById('startingPoint').value;
    const genBtn = document.querySelector('button[onclick="generateItinerary()"]');
    if (!startingPoint) {
      alert('Please enter a starting point');
      return;
    }
    // Disable button and show loading
    if (genBtn) {
      genBtn.disabled = true;
      genBtn.classList.add('btn-loading');
    }
    const container = document.getElementById('itineraryDays');
    container.innerHTML = `
      <div class="itinerary-loading-container">
        <div class="loading-animation">
          <div class="loading-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
          </div>
        </div>
        <div class="loading-content">
          <h4 class="loading-title">
            <i class="fas fa-magic"></i> Crafting Your Perfect Itinerary
          </h4>
          <div class="loading-steps">
            <div class="loading-step active">
              <i class="fas fa-search"></i>
              <span>Analyzing preferences...</span>
            </div>
            <div class="loading-step">
              <i class="fas fa-map-marked-alt"></i>
              <span>Optimizing routes...</span>
            </div>
            <div class="loading-step">
              <i class="fas fa-calendar-check"></i>
              <span>Building schedule...</span>
            </div>
          </div>
          <div class="loading-progress">
            <div class="progress-bar">
              <div class="progress-fill"></div>
            </div>
          </div>
        </div>
      </div>`;
    startLoadingAnimation();

    setTimeout(() => {
      // Use all available places from window.PLACES_WITH_WEATHER
      const places = (window.PLACES_WITH_WEATHER || []).map(p => ({
        id: p.id,
        name: p.name,
        category: p.category,
        description: p.description,
        location: p.location,
        latitude: p.latitude,
        longitude: p.longitude
      }));
      // Find starting point coordinates
      const startingPlace = places.find(p =>
        p.name.toLowerCase().includes(startingPoint.toLowerCase()) ||
        startingPoint.toLowerCase().includes(p.name.toLowerCase())
      );
      const latitude = startingPlace ? startingPlace.latitude : 12.9716; // Default to Bengaluru
      const longitude = startingPlace ? startingPlace.longitude : 77.5946;
      // Build Gemini AI URL
      const geminiUrl = (window.GEMINI_RECOMMENDATIONS_URL || '/state/get-gemini-recommendations/') +
        `?latitude=${latitude}&longitude=${longitude}` +
        `&user_place=${encodeURIComponent(startingPoint)}` +
        `&place_type=tourist_attraction&budget=${style}&duration=${duration}` +
        `&itinerary=true&travel_style=${style}&trip_duration=${duration}&context=karnataka`;
      fetch(geminiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
      })
      .then(data => {
        // Get AI recommended places and match them to real places by name
        const aiPlaces = data.gemini_recommended_places || [];
        
        // Simple success message
        const container = document.getElementById('itineraryDays');
        container.innerHTML = `
          <div class="alert alert-success mb-4">
            <i class="fas fa-check-circle"></i>
            Your ${duration}-day ${style} itinerary is ready!
          </div>
        `;
        
        const itineraryDays = createSmartItinerary(duration, style, startingPoint, places, aiPlaces);
        
        // Display the itinerary
        displayItinerary(itineraryDays, startingPoint);
        
        const generatedItineraryDiv = document.getElementById('generatedItinerary');
        if (generatedItineraryDiv) generatedItineraryDiv.classList.remove('d-none');
        // Re-enable button
        if (genBtn) {
          genBtn.disabled = false;
          genBtn.classList.remove('btn-loading');
        }
        // Smooth scroll to results
        setTimeout(() => {
          document.getElementById('generatedItinerary').scrollIntoView({ behavior: 'smooth' });
        }, 100);
      })
      .catch(error => {
        console.warn('AI recommendation failed, falling back to local places:', error);
        
        // Simple fallback message
        const container = document.getElementById('itineraryDays');
        container.innerHTML = `
          <div class="alert alert-info mb-4">
            <i class="fas fa-info-circle"></i>
            Using our local database to create your ${duration}-day ${style} itinerary.
          </div>
        `;
        
        // Create itinerary with local places only
        const itineraryDays = createSmartItinerary(duration, style, startingPoint, places, []);
        
        // Display the itinerary
        displayItinerary(itineraryDays, startingPoint);
        
        const generatedItineraryDiv = document.getElementById('generatedItinerary');
        if (generatedItineraryDiv) generatedItineraryDiv.classList.remove('d-none');
        if (genBtn) {
          genBtn.disabled = false;
          genBtn.classList.remove('btn-loading');
        }
        setTimeout(() => {
          document.getElementById('generatedItinerary').scrollIntoView({ behavior: 'smooth' });
        }, 100);
      });
    }, 400);
  };

  function startLoadingAnimation() {
    const steps = document.querySelectorAll('.loading-step');
    const progressFill = document.querySelector('.progress-fill');
    let currentStep = 0;
    function nextStep() {
      if (steps[currentStep]) steps[currentStep].classList.remove('active');
      currentStep++;
      if (steps[currentStep]) steps[currentStep].classList.add('active');
      if (progressFill) progressFill.style.width = ((currentStep + 1) / steps.length * 100) + '%';
      if (currentStep < steps.length - 1) {
        setTimeout(nextStep, 400);
      }
    }
    setTimeout(nextStep, 400);
  }

  function createSmartItinerary(duration, style, startingPoint, places, aiPlaces) {
    const itineraryDays = [];
    
    const aiPlaceMap = new Map((aiPlaces || []).map(place => [place.name.toLowerCase(), {
      ...place,
      reasoning: place.reasoning || 'Recommended based on your preferences'
    }]));
    
    const combinedPlaces = new Map();
    places.forEach(p => combinedPlaces.set(p.name.toLowerCase(), p));
    aiPlaces.forEach(p => {
        combinedPlaces.set(p.name.toLowerCase(), {
            ...p,
            latitude: p.latitude || null,
            longitude: p.longitude || null,
        });
    });
    const allPlaces = Array.from(combinedPlaces.values());

    let availablePlaces = filterPlacesByStyle(allPlaces, style);

    if (availablePlaces.length < duration) {
        availablePlaces = allPlaces;
    }
  
    let shuffledPlaces = shuffleArray(availablePlaces);
    const placesPerDay = Math.ceil(shuffledPlaces.length / duration);
  
    for (let day = 1; day <= duration; day++) {
      // Use splice to get a chunk of places and remove them from the array
      const dayPlaces = shuffledPlaces.splice(0, placesPerDay);
      
      if (dayPlaces.length > 0) {
        itineraryDays.push({
          day,
          places: dayPlaces,
          aiInsights: dayPlaces.map(place => aiPlaceMap.get(place.name.toLowerCase()) || null).filter(Boolean)
        });
      }
    }
    
    return itineraryDays;
  }

  function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  function filterPlacesByStyle(places, style) {
    return places.filter(p => {
        const name = p.name.toLowerCase();
        const category = (p.category || '').toLowerCase();
        switch (style) {
            case 'adventure':
                return ['adventure', 'park', 'hill', 'wildlife', 'forest', 'waterfall', 'trek', 'climbing'].some(c =>
                    category.includes(c) || name.includes(c)
                );
            case 'cultural':
                return ['temple', 'museum', 'cultural', 'historical', 'fort', 'palace', 'heritage', 'monument'].some(c =>
                    category.includes(c) || name.includes(c)
                );
            case 'relaxation':
                return ['beach', 'hill', 'garden', 'lake', 'resort', 'spa', 'wellness', 'meditation'].some(c =>
                    category.includes(c) || name.includes(c)
                );
            case 'luxury':
                return ['resort', 'spa', 'hotel', 'palace', 'heritage', 'premium', 'exclusive'].some(c =>
                    category.includes(c) || name.includes(c)
                );
            default:
                return true;
        }
    });
  }

  function displayItinerary(itineraryDays, startingPoint) {
    const container = document.getElementById('itineraryDays');
    if (!container) return;

    // Build the HTML for the itinerary
    const itineraryHtml = itineraryDays.map(dayData => `
        <div class="itinerary-day">
            <h6><i class="fas fa-calendar-day"></i> Day ${dayData.day}</h6>
            ${dayData.day === 1 ? `<p class="text-muted mb-3"><i class="fas fa-map-marker-alt"></i> Starting from: ${startingPoint}</p>` : ''}
            ${dayData.places.map((place, index) => {
                const aiInsight = dayData.aiInsights[index];
                // Conditionally render the map button
                const mapButton = (place.latitude && place.longitude)
                    ? `<button class="btn btn-outline-primary btn-sm ms-2" onclick="showPlaceOnMap('${place.latitude}', '${place.longitude}', '${place.name.replace(/'/g, "\\'")}')">
                           <i class="fas fa-map-marker-alt"></i> Show on Map
                       </button>`
                    : '';
                return `
                    <div class="itinerary-place">
                        <div class="place-details">
                            <strong>${place.name}</strong>
                            <small class="text-muted d-block">${place.category || 'Recommended Place'}</small>
                            ${aiInsight ? `
                                <div class="ai-insight mt-2">
                                    <i class="fas fa-robot text-primary"></i>
                                    <small class="text-primary">AI Insight: ${aiInsight.reasoning}</small>
                                </div>` : ''}
                        </div>
                        ${mapButton}
                    </div>
                `;
            }).join('')}
        </div>
    `).join('');

    // Append the itinerary to the success message
    container.innerHTML += itineraryHtml;
  }

  // --- ITINERARY BUTTONS ---
  window.saveItinerary = function() {
    const itineraryDiv = document.getElementById('itineraryDays');
    if (!itineraryDiv) return alert('No itinerary to save!');
    // Extract day-wise descriptions
    const days = Array.from(itineraryDiv.querySelectorAll('.itinerary-day')).map((el, idx) => ({
      day: idx + 1,
      description: el.innerText.trim()
    }));
    if (!days.length) return alert('No itinerary to save!');
    // Get state_id from a global JS variable or data attribute
    const stateId = window.STATE_ID || document.body.dataset.stateId || null;
    if (!stateId) return alert('State ID not found!');
    fetch('/core/save-itinerary/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': (document.querySelector('[name=csrfmiddlewaretoken]')||{}).value || ''
      },
      body: JSON.stringify({ state_id: stateId, days })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Itinerary saved! View it in your profile.');
      } else {
        alert('Failed to save itinerary: ' + (data.error || 'Unknown error'));
      }
    })
    .catch(err => alert('Error saving itinerary: ' + err.message));
  };

  window.exportItinerary = function() {
    // For demo: print the itinerary section as PDF
    const itineraryDiv = document.getElementById('generatedItinerary');
    if (!itineraryDiv) return alert('No itinerary to export!');
    const printContents = itineraryDiv.innerHTML;
    const win = window.open('', '', 'height=700,width=900');
    win.document.write('<html><head><title>Exported Itinerary</title>');
    win.document.write('<link rel="stylesheet" href="/static/core/css/style.css">');
    win.document.write('</head><body >');
    win.document.write(printContents);
    win.document.write('</body></html>');
    win.document.close();
    win.focus();
    setTimeout(() => { win.print(); win.close(); }, 500);
  };

  window.resetItinerary = function() {
    const itineraryDiv = document.getElementById('generatedItinerary');
    const daysDiv = document.getElementById('itineraryDays');
    if (daysDiv) daysDiv.innerHTML = '';
    if (itineraryDiv) itineraryDiv.classList.add('d-none');
  };

  // --- RUN INITIALIZATION ---
  initializePage();
});