// tamil_nadu.js - All Tamil Nadu page-specific JS logic
(function() {
  // --- GLOBAL/MODULE-LEVEL VARIABLES ---
  const geminiApiUrl = "/state/get-gemini-recommendations/";
  let mapModalInstance = null;
  let modalMap = null;
  let modalMarker = null;

  // --- Review System ---
  let selectedRating = 0;
  document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    
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
  });

  // --- PRIMARY INITIALIZATION ---
  function initializePage() {
    initializeAOS();
    initializeNavbarScroll();
    initializeBackToTopButton();
    initializeCategoryFilter();
    initializeCalendar();
    initializeMapModal();
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
    if (!mapModalInstance) initializeMapModal();
    if (!mapModalInstance || !lat || !lng) {
      console.error("Map modal or coordinates not available.");
      return;
    }
    
    mapModalInstance.show();
    
    const position = { lat: parseFloat(lat), lng: parseFloat(lng) };
    const modalTitle = document.getElementById('mapModalLabel');
    if(modalTitle) modalTitle.textContent = name;

    // Always re-create the map and marker for each place
    setTimeout(() => {
      const mapContainer = document.getElementById('modalMapContainer');
      if (mapContainer) {
        // Remove any previous map instance by clearing the container
        mapContainer.innerHTML = '';
        modalMap = new google.maps.Map(mapContainer, {
          zoom: 15,
          center: position,
          mapTypeControl: false,
          streetViewControl: true,
          fullscreenControl: true,
        });
        modalMarker = new google.maps.Marker({
          position: position,
          map: modalMap,
          title: name,
          animation: google.maps.Animation.DROP,
        });
        google.maps.event.trigger(modalMap, 'resize');
        modalMap.setCenter(position);
      }
    }, 300); // Wait for modal animation
  };

  // --- EVENTS CALENDAR LOGIC ---
  function initializeCalendar() {
    const events = [
      { date: new Date('2025-01-14'), title: 'Pongal', place: 'Throughout Tamil Nadu', description: 'Harvest festival celebrated with traditional cooking and thanksgiving.' },
      { date: new Date('2025-04-14'), title: 'Tamil New Year', place: 'Throughout Tamil Nadu', description: 'Tamil New Year celebrated with traditional rituals and feasts.' },
      { date: new Date('2025-08-15'), title: 'Independence Day', place: 'Throughout Tamil Nadu', description: 'National celebration with flag hoisting and cultural programs.' },
      { date: new Date('2025-09-17'), title: 'Vinayagar Chaturthi', place: 'Throughout Tamil Nadu', description: 'Festival dedicated to Lord Ganesha with processions and prayers.' },
      { date: new Date('2025-10-24'), title: 'Navaratri', place: 'Throughout Tamil Nadu', description: 'Nine nights of devotion with traditional music and dance.' },
      { date: new Date('2025-11-12'), title: 'Diwali', place: 'Throughout Tamil Nadu', description: 'Festival of lights celebrated with fireworks and sweets.' }
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

    function renderEvents() {
      let html = '<h3>Events & Festivals</h3>';
      if (!selectedDate) {
        html += '<div id="eventPrompt" class="event-item"><p>Please select a date on the calendar to view events or festivals.</p></div>';
      } else {
        const filteredEvents = events.filter(ev => ev.date.toDateString() === selectedDate.toDateString());
        if (filteredEvents.length === 0) {
          html += '<div class="event-item"><p>No events or festivals for this date.</p></div>';
        } else {
          filteredEvents.forEach(ev => {
            html += `<div class="event-item">
              <h4>${ev.title} <span class="event-date">(${ev.date.toLocaleDateString('en-IN')})</span></h4>
              <p><strong>Location:</strong> ${ev.place}</p>
              <p>${ev.description}</p>
            </div>`;
          });
        }
      }
      elements.eventList.innerHTML = html;
    }

    function changeMonth(offset) {
      currentDate.setMonth(currentDate.getMonth() + offset);
      selectedDate = null;
      renderCalendar();
      renderEvents();
    }

    // Initialize calendar
    renderCalendar();
    renderEvents();

    // Event listeners
    elements.grid.addEventListener('click', function(e) {
      if (e.target.classList.contains('calendar-cell') && e.target.dataset.date) {
        selectedDate = new Date(e.target.dataset.date);
        renderCalendar();
        renderEvents();
      }
    });

    if (elements.prevBtn) elements.prevBtn.addEventListener('click', () => changeMonth(-1));
    if (elements.nextBtn) elements.nextBtn.addEventListener('click', () => changeMonth(1));
  }

  // --- REVIEW SYSTEM ---
  function submitReview(placeId, rating, comment) {
    const csrfToken = window.CSRF_TOKEN;
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

  // --- AI RECOMMENDATIONS LOGIC ---
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
        context: 'tamil_nadu'
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
      recommendationsDiv.innerHTML = `<div class="alert alert-info m-3">No recommendations found for your current location and preferences.</div>`;
      return;
    }

    let html = '<div class="row">';
    places.forEach(place => {
      const escapedName = place.name.replace(/'/g, "\\'");
      html += `
        <div class="col-md-6 col-lg-4 mb-4">
          <div class="card h-100 recommendation-card">
            <div class="card-body">
              <h5 class="card-title">${place.name}</h5>
              <p class="card-text">${place.reasoning || 'Recommended based on your preferences'}</p>
              ${place.latitude && place.longitude ? `<button class="btn btn-primary" onclick="showPlaceOnMap('${place.latitude}', '${place.longitude}', '${escapedName}')">
                <i class="fas fa-map-marker-alt"></i> Show on Map
              </button>` : ''}
            </div>
          </div>
        </div>
      `;
    });
    html += '</div>';

    if (weatherData) {
      html = `<div class="weather-info mb-4">
        <div class="alert alert-info">
          <h6><i class="fas fa-cloud-sun"></i> Current Weather</h6>
          <p class="mb-1">Temperature: ${weatherData.temperature}°C | Condition: ${weatherData.condition}</p>
          <small>${weatherData.suggestions ? weatherData.suggestions.join(' ') : ''}</small>
        </div>
      </div>` + html;
    }

    recommendationsDiv.innerHTML = html;
  }

  window.clearRecommendations = function() {
    const recommendationsDiv = document.getElementById("gemini-recommended-places");
    if (recommendationsDiv) {
      recommendationsDiv.innerHTML = `
        <div class="text-center py-5">
          <div class="recommendation-placeholder">
            <i class="fas fa-compass fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">Ready to Discover?</h5>
            <p class="text-muted">Select your preferences above and get personalized recommendations</p>
          </div>
        </div>
      `;
    }
  };

  // --- ITINERARY BUILDER LOGIC ---
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
      const latitude = startingPlace ? startingPlace.latitude : 13.0827; // Default to Chennai
      const longitude = startingPlace ? startingPlace.longitude : 80.2707;
      
      // Build Gemini AI URL
      const geminiUrl = (window.GEMINI_RECOMMENDATIONS_URL || '/state/get-gemini-recommendations/') +
        `?latitude=${latitude}&longitude=${longitude}` +
        `&user_place=${encodeURIComponent(startingPoint)}` +
        `&place_type=tourist_attraction&budget=${style}&duration=${duration}` +
        `&itinerary=true&travel_style=${style}&trip_duration=${duration}&context=tamil_nadu`;
      
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
        const aiPlaces = data.gemini_recommended_places || [];
        const itineraryDays = createSmartItinerary(duration, style, startingPoint, places, aiPlaces);
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
        console.warn('AI recommendation failed, falling back to smart itinerary:', error);
        const itineraryDays = createSmartItinerary(duration, style, startingPoint, places, []);
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
    
    let allPlaces = [...places];
    if (aiPlaces && aiPlaces.length > 0) {
      const aiPlaceNames = new Set(aiPlaces.map(p => p.name.toLowerCase()));
      const aiMatchedPlaces = places.filter(p => aiPlaceNames.has(p.name.toLowerCase()));
      const otherPlaces = places.filter(p => !aiPlaceNames.has(p.name.toLowerCase()));
      allPlaces = [...aiMatchedPlaces, ...otherPlaces];
    }
    
    let filteredPlaces = filterPlacesByStyle(allPlaces, style);
    
    for (let day = 1; day <= duration; day++) {
      const dayPlaces = getDiversePlacesForDay(filteredPlaces, day, duration);
      itineraryDays.push({
        day: day,
        places: dayPlaces,
        startingPoint: day === 1 ? startingPoint : null
      });
    }
    
    return itineraryDays;
  }

  function filterPlacesByStyle(places, style) {
    const styleFilters = {
      'cultural': ['temple', 'museum', 'historical', 'cultural'],
      'adventure': ['adventure', 'trek', 'hiking', 'waterfall'],
      'relaxation': ['beach', 'hill', 'garden', 'park'],
      'family': ['park', 'museum', 'beach', 'garden'],
      'budget': ['temple', 'park', 'beach', 'garden'],
      'luxury': ['resort', 'spa', 'palace', 'heritage']
    };
    
    const keywords = styleFilters[style] || ['temple', 'beach', 'hill', 'museum'];
    return places.filter(place => 
      keywords.some(keyword => 
        place.name.toLowerCase().includes(keyword) || 
        place.category.toLowerCase().includes(keyword)
      )
    );
  }

  function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }

  function getDiversePlacesForDay(filteredPlaces, day, duration) {
    const categories = ['temple', 'beach', 'hill', 'museum', 'park', 'fort', 'palace', 'garden', 'market', 'resort'];
    const dayPlaces = [];
    
    // Ensure each day has different types of places
    const categoryRotation = categories.slice((day - 1) % categories.length);
    
    categoryRotation.forEach(category => {
      const categoryPlaces = filteredPlaces.filter(p => 
        p.name.toLowerCase().includes(category) || 
        p.category.toLowerCase().includes(category)
      );
      
      if (categoryPlaces.length > 0) {
        // Add 1-2 places from this category
        const sample = shuffleArray(categoryPlaces).slice(0, 2);
        dayPlaces.push(...sample);
      }
    });
    
    // If we don't have enough places, add random ones
    if (dayPlaces.length < 2) {
      const remainingPlaces = filteredPlaces.filter(p => !dayPlaces.some(dp => dp.id === p.id));
      dayPlaces.push(...shuffleArray(remainingPlaces).slice(0, 2 - dayPlaces.length));
    }
    
    return shuffleArray(dayPlaces);
  }

  function displayItinerary(itineraryDays, startingPoint) {
    const container = document.getElementById('itineraryDays');
    let html = '';
    
    itineraryDays.forEach(day => {
      html += `
        <div class="itinerary-day mb-4">
          <h4 class="day-title">
            <i class="fas fa-calendar-day"></i> Day ${day.day}
            ${day.startingPoint ? `<span class="starting-point">Starting from: ${day.startingPoint}</span>` : ''}
          </h4>
          <div class="day-places">
      `;
      
      day.places.forEach(place => {
        const escapedName = place.name.replace(/'/g, "\\'");
        html += `
          <div class="place-item">
            <h5>${place.name}</h5>
            <p>${place.description}</p>
            ${place.latitude && place.longitude ? `<button class="btn btn-outline-primary btn-sm ms-2" onclick="showPlaceOnMap('${place.latitude}', '${place.longitude}', '${escapedName}')">
              <i class="fas fa-map-marker-alt"></i> Show on Map
            </button>` : ''}
          </div>
        `;
      });
      
      html += `
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  }

  // --- AI-Powered Recommendations Deduplication Example ---
  function renderGeminiRecommendations(places, weatherData) {
    // Deduplicate by place name
    const uniquePlaces = [];
    const seenNames = new Set();
    places.forEach(place => {
      if (!seenNames.has(place.name)) {
        uniquePlaces.push(place);
        seenNames.add(place.name);
      }
    });
    // ... render uniquePlaces instead of places ...
    // (Insert your rendering logic here, using uniquePlaces)
  }

  // --- FAVORITES MANAGEMENT ---

  window.addToFavorites = function(name, latitude, longitude, event) {
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
      alert('CSRF token not found. Please refresh the page and try again.');
      return;
    }
    
    fetch('/add-recommended-favorite/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        name: name,
        latitude: latitude,
        longitude: longitude
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      if (data.success) {
        const button = event.target;
        button.innerHTML = '<i class="fas fa-heart"></i> Added to Favorites';
        button.classList.add('favorited');
        button.disabled = true;
        
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show position-fixed';
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
          <i class="fas fa-check-circle"></i> ${name} added to favorites!
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
          if (alertDiv.parentNode) {
            alertDiv.remove();
          }
        }, 3000);
      } else {
        alert('Error adding to favorites: ' + (data.error || 'Unknown error'));
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error adding to favorites: ' + error.message);
    });
  };

  // --- CSRF TOKEN HELPER ---

  function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
})(); 