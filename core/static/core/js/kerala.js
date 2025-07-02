// static/core/js/kerala.js
// This file contains all the client-side JavaScript logic for the enhanced Kerala state page.

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
        { date: new Date('2025-01-14'), title: 'Makaravilakku', place: 'Sabarimala', description: 'Sacred festival at Sabarimala temple with divine light appearance.' },
        { date: new Date('2025-04-14'), title: 'Vishu', place: 'Throughout Kerala', description: 'Kerala New Year celebrated with Vishu Kani and traditional feast.' },
        { date: new Date('2025-08-15'), title: 'Onam', place: 'Throughout Kerala', description: 'Harvest festival celebrating King Mahabali with boat races and feasts.' },
        { date: new Date('2025-09-17'), title: 'Thrissur Pooram', place: 'Thrissur', description: 'Grand temple festival with spectacular elephant processions.' },
        { date: new Date('2025-10-24'), title: 'Navaratri', place: 'Throughout Kerala', description: 'Nine nights of devotion with traditional music and dance.' },
        { date: new Date('2025-11-12'), title: 'Diwali', place: 'Throughout Kerala', description: 'Festival of lights celebrated with fireworks and sweets.' }
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
      // Remove the allowed_places restriction to allow broader recommendations
      const params = new URLSearchParams({
          latitude,
          longitude,
          user_place: selectedOption.value,
          place_type: placeType,
          budget,
          duration,
          enhanced: 'true',
          context: 'kerala' // CRITICAL: This provides context to the AI
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
      if (data.error) {
        recommendationsDiv.innerHTML = `<div class="alert alert-info m-3">${data.error}</div>`;
        return;
      }
      const places = data.gemini_recommended_places;
      const weather = data.weather_data || {};
      if (!places || places.length === 0) {
          recommendationsDiv.innerHTML = `<div class="alert alert-info m-3">No recommendations found. Please try different filters.</div>`;
          return;
      }
      // Track favorites in-memory for this session (for demo; ideally, fetch from backend)
      let favoriteNames = window.FAVORITE_PLACE_NAMES || [];
      let html = '<div class="row p-3">';
      places.forEach(place => {
        const escapedName = place.name.replace(/'/g, "\\'").replace(/"/g, '"');
        const rating = place.rating || 'N/A';
        const reasoning = place.reasoning || 'No description available';
        html += `
          <div class="col-md-6 mb-4">
            <div class="card recommendation-card h-100 shadow-sm border-0">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title mb-2">${place.name}</h5>
                <span class="recommendation-badge mb-2"><i class="fas fa-star"></i> Rating: ${rating}</span>
                <div class="recommendation-weather mb-2 p-2 rounded bg-light">
                  <div><i class="fas fa-thermometer-half text-primary"></i> <b>Temperature:</b> ${weather.temperature ?? 'N/A'}°C</div>
                  <div><i class="fas fa-tint text-info"></i> <b>Humidity:</b> ${weather.humidity ?? 'N/A'}%</div>
                  <div><i class="fas fa-cloud text-secondary"></i> <b>Condition:</b> ${weather.description ?? 'N/A'}</div>
                </div>
                <div class="location-info mb-2 text-muted small">
                  <i class="fas fa-map-marker-alt"></i> ${place.latitude?.toFixed(4) ?? 'N/A'}, ${place.longitude?.toFixed(4) ?? 'N/A'}
                </div>
                <p class="reasoning mb-2"><em>"${reasoning}"</em></p>
                <div class="mt-auto pt-2 d-flex gap-2">
                  <button class="btn btn-primary flex-fill" onclick="showOnMap('${place.latitude}', '${place.longitude}', '${escapedName}')">
                    <i class="fas fa-map-marker-alt"></i> View on Map
                  </button>
                  <button class="btn btn-outline-secondary flex-fill" onclick="addToFavorites('${escapedName}', ${place.latitude}, ${place.longitude}, this)">
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
  
    // Add to Favorites logic for AI-recommended places
    window.addToFavorites = function(name, latitude, longitude, btn) {
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
        body: JSON.stringify({ name, latitude, longitude })
      })
      .then(async response => {
        const contentType = response.headers.get('content-type');
        let data = null;
        if (contentType && contentType.includes('application/json')) {
          data = await response.json();
        } else {
          throw new Error('Unexpected server response. Please log in and try again.');
        }
        if (data.success) {
          btn.classList.remove('btn-outline-secondary');
          btn.classList.add('btn-success');
          btn.disabled = true;
          btn.innerHTML = '<i class="fas fa-heart"></i> Added to Favorites';
          window.FAVORITE_PLACE_NAMES = (window.FAVORITE_PLACE_NAMES || []);
          if (!window.FAVORITE_PLACE_NAMES.includes(name)) window.FAVORITE_PLACE_NAMES.push(name);
          showToast('Added to favorites!', 'success');
        } else {
          showToast('Error adding to favorites: ' + (data.error || 'Unknown error'), 'danger');
        }
      })
      .catch(error => {
        showToast('Error adding to favorites: ' + error.message, 'danger');
      });
    };
    window.removeFromFavorites = function(name, latitude, longitude, btn) {
      btn.classList.remove('btn-danger');
      btn.classList.add('btn-outline-secondary');
      btn.innerHTML = '<i class="far fa-heart"></i> Save';
      btn.onclick = function() { addToFavorites(name, latitude, longitude, btn); };
      window.FAVORITE_PLACE_NAMES = (window.FAVORITE_PLACE_NAMES || []).filter(n => n !== name);
      showToast('Removed from favorites.', 'info');
    };
    // Toast feedback
    function showToast(message, type) {
      let toast = document.getElementById('gemini-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'gemini-toast';
        toast.className = 'toast align-items-center text-bg-' + type + ' border-0 position-fixed top-0 end-0 m-4';
        toast.style.zIndex = 2000;
        toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.remove()"></button></div>`;
        document.body.appendChild(toast);
      } else {
        toast.querySelector('.toast-body').textContent = message;
        toast.className = 'toast align-items-center text-bg-' + type + ' border-0 position-fixed top-0 end-0 m-4';
      }
      toast.style.display = 'block';
      setTimeout(() => { if (toast) toast.style.display = 'none'; }, 3000);
    }
  
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
        // Prevent double submission
        if (addReviewForm.classList.contains('submitting')) return;
        addReviewForm.classList.add('submitting');
        submitReview(placeId, selectedRating, comment);
      });
    }
    function submitReview(placeId, rating, comment) {
      const csrfToken = getCSRFToken();
      if (!csrfToken) {
        alert('CSRF token not found. Please refresh the page and try again.');
        const addReviewForm = document.getElementById('addReviewForm');
        if (addReviewForm) addReviewForm.classList.remove('submitting');
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
      })
      .finally(() => {
        const addReviewForm = document.getElementById('addReviewForm');
        if (addReviewForm) addReviewForm.classList.remove('submitting');
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
        const latitude = startingPlace ? startingPlace.latitude : 9.9312; // Default to Kochi
        const longitude = startingPlace ? startingPlace.longitude : 76.2673;
        // Build Gemini AI URL
        const geminiUrl = (window.GEMINI_RECOMMENDATIONS_URL || '/state/get-gemini-recommendations/') +
          `?latitude=${latitude}&longitude=${longitude}` +
          `&user_place=${encodeURIComponent(startingPoint)}` +
          `&place_type=tourist_attraction&budget=${style}&duration=${duration}` +
          `&itinerary=true&travel_style=${style}&trip_duration=${duration}&context=kerala`;
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
      const categories = ['temple', 'beach', 'hill', 'museum', 'park', 'fort', 'palace', 'garden', 'market', 'resort'];
      const categoryPlaces = {};
      categories.forEach(category => {
        categoryPlaces[category] = allPlaces.filter(p =>
          p.name.toLowerCase().includes(category) ||
          (p.category && p.category.toLowerCase().includes(category))
        );
      });
      if (filteredPlaces.length < duration * 3) {
        const additionalPlaces = [];
        categories.forEach(category => {
          if (categoryPlaces[category].length > 0) {
            const categorySample = categoryPlaces[category].slice(0, 2);
            additionalPlaces.push(...categorySample);
          }
        });
        const uniqueAdditional = additionalPlaces.filter(p =>
          !filteredPlaces.some(fp => fp.id === p.id)
        );
        filteredPlaces = [...filteredPlaces, ...uniqueAdditional];
      }
      filteredPlaces = shuffleArray(filteredPlaces);
      for (let day = 1; day <= duration; day++) {
        const dayPlaces = getDiversePlacesForDay(filteredPlaces, day, duration);
        if (dayPlaces.length > 0) {
          itineraryDays.push({
            day,
            places: dayPlaces,
            aiInsights: dayPlaces.map(place => aiPlaceMap.get(place.name.toLowerCase()) || null).filter(Boolean)
          });
        }
      }
      while (itineraryDays.length < duration) {
        const remainingPlaces = filteredPlaces.filter(p =>
          !itineraryDays.some(day => day.places.find(dp => dp.id === p.id))
        );
        if (remainingPlaces.length === 0) break;
        const dayPlaces = shuffleArray(remainingPlaces).slice(0, 2);
        itineraryDays.push({
          day: itineraryDays.length + 1,
          places: dayPlaces,
          aiInsights: []
        });
      }
      return itineraryDays;
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
  
    function shuffleArray(array) {
      const shuffled = [...array];
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
      }
      return shuffled;
    }
  
    function getDiversePlacesForDay(filteredPlaces, day, duration) {
      const perDay = Math.ceil(filteredPlaces.length / duration);
      const start = (day - 1) * perDay;
      return filteredPlaces.slice(start, start + perDay);
    }
  
    function displayItinerary(itineraryDays, startingPoint) {
      const container = document.getElementById('itineraryDays');
      let html = itineraryDays.map(dayData => `
        <div class="itinerary-day">
          <h6><i class="fas fa-calendar-day"></i> Day ${dayData.day}</h6>
          ${dayData.day === 1 ? `<p class="text-muted mb-3"><i class="fas fa-map-marker-alt"></i> Starting from: ${startingPoint}</p>` : ''}
          ${dayData.places.map((place, index) => {
            const aiInsight = dayData.aiInsights[index];
            return `
              <div class="itinerary-place">
                <div class="place-details">
                  <strong>${place.name}</strong>
                  <small class="text-muted d-block">${place.category}</small>
                  ${aiInsight ? `
                    <div class="ai-insight mt-2">
                      <i class="fas fa-robot text-primary"></i>
                      <small class="text-primary">AI Insight: ${aiInsight.reasoning}</small>
                    </div>` : ''}
                </div>
                <button class="btn btn-outline-primary btn-sm ms-2" onclick="showOnMap('${place.latitude}', '${place.longitude}', '${place.name.replace(/'/g, "\\'")}')">
                  <i class="fas fa-map-marker-alt"></i> Show on Map
                </button>
              </div>
            `;
          }).join('')}
        </div>
      `).join('');
      container.innerHTML = html;
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