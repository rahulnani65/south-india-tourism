// static/core/js/andhra_pradesh.js
document.addEventListener('DOMContentLoaded', function() {
    'use strict';
  
    const geminiApiUrl = window.GEMINI_RECOMMENDATIONS_URL || "/state/get-gemini-recommendations/";
  
    function initializePage() {
      initializeAOS();
      initializeNavbarScroll();
      initializeBackToTopButton();
      initializeCategoryFilter();
      initializeCalendar();
      initializeReviewSystem();
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
      filter.addEventListener('change', filterPlacesByCategory); filterPlacesByCategory();
    }
    function filterPlacesByCategory() {
      const category = document.getElementById('categoryFilter').value;
      const cards = document.querySelectorAll('.place-card-wrapper'); let count = 0;
      cards.forEach(card => {
        const cardCat = card.dataset.category || 'all';
        const show = (category === 'all' || cardCat.includes(category));
        card.style.display = show ? 'block' : 'none'; if (show) count++;
      });
      const countEl = document.getElementById('place-count'); if(countEl) countEl.innerHTML = `<small>Showing ${count} of ${cards.length} places</small>`;
    }
    
    let mainPlacesMap = null, mainPlacesMarker = null, mainPlacesMapModalInstance = null;
    window.showPlaceOnMap = function(latitude, longitude, placeName) {
      if (!mainPlacesMapModalInstance) {
        const modalEl = document.getElementById('mainPlacesMapModal');
        if (!modalEl) return console.error('Modal with ID mainPlacesMapModal not found!');
        mainPlacesMapModalInstance = new bootstrap.Modal(modalEl);
      }
      mainPlacesMapModalInstance.show();
      const modalTitle = document.getElementById('mainPlacesMapModalLabel');
      if(modalTitle) modalTitle.textContent = placeName;
      if (!mainPlacesMap) {
        mainPlacesMap = new google.maps.Map(document.getElementById('mainPlacesMap'), { zoom: 15, mapTypeControl: true, streetViewControl: true, fullscreenControl: true });
      }
      const position = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
      mainPlacesMap.setCenter(position);
      if (mainPlacesMarker) mainPlacesMarker.setMap(null);
      mainPlacesMarker = new google.maps.Marker({ position, map: mainPlacesMap, title: placeName, animation: google.maps.Animation.DROP });
    };
    const mainMapModalEl = document.getElementById('mainPlacesMapModal');
    if (mainMapModalEl) mainMapModalEl.addEventListener('shown.bs.modal', () => { if (mainPlacesMap) { google.maps.event.trigger(mainPlacesMap, 'resize'); if (mainPlacesMarker) mainPlacesMap.setCenter(mainPlacesMarker.getPosition()); } });
  
    function initializeCalendar() {
        // Andhra Pradesh specific events
        const events = [
            { date: new Date(new Date().getFullYear(), 0, 14), title: 'Makar Sankranti', place: 'Throughout Andhra Pradesh', description: 'A grand harvest festival celebrated with kite flying, bonfires, and traditional feasts.' },
            { date: new Date(new Date().getFullYear(), 2, 22), title: 'Ugadi', place: 'Throughout Andhra Pradesh', description: 'The Telugu New Year, marked by the special "Ugadi Pachadi" dish symbolizing life\'s different flavors.' },
            { date: new Date(new Date().getFullYear(), 3, 10), title: 'Sri Rama Navami', place: 'Bhadrachalam & other temples', description: 'Celebrates the birth of Lord Rama with elaborate ceremonies and processions.' },
            { date: new Date(new Date().getFullYear(), 9, 12), title: 'Dussehra (Vijayadashami)', place: 'Vijayawada', description: 'A major festival celebrating the victory of good over evil, with special festivities at Kanaka Durga Temple.' },
            { date: new Date(new Date().getFullYear(), 11, 25), title: 'Lumbini Festival', place: 'Nagarjunakonda', description: 'A Buddhist festival celebrating the rich heritage of the region, usually held in December.' }
        ];
        let currentDate = new Date(), selectedDate = null;
        const els = { grid: document.getElementById('calendarGrid'), monthYear: document.getElementById('calendarMonthYear'), eventList: document.getElementById('eventList'), prevBtn: document.getElementById('calendarPrev'), nextBtn: document.getElementById('calendarNext'), prompt: document.getElementById('eventPrompt') };
        if (!els.grid) return;
        function renderCalendar() {
          const month = currentDate.getMonth(), year = currentDate.getFullYear();
          els.monthYear.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;
          els.grid.innerHTML = '';
          const firstDay = new Date(year, month, 1).getDay(), daysInMonth = new Date(year, month + 1, 0).getDate(), today = new Date();
          for (let i = 0; i < firstDay; i++) els.grid.insertAdjacentHTML('beforeend', '<div></div>');
          for (let d = 1; d <= daysInMonth; d++) {
            const cellDate = new Date(year, month, d), hasEvent = events.some(ev => ev.date.toDateString() === cellDate.toDateString());
            let classes = 'calendar-cell';
            if (hasEvent) classes += ' event-day';
            if (cellDate.toDateString() === today.toDateString()) classes += ' today';
            if (selectedDate && cellDate.toDateString() === selectedDate.toDateString()) classes += ' selected';
            els.grid.insertAdjacentHTML('beforeend', `<div class="${classes}" data-date="${cellDate.toISOString()}">${d}${hasEvent ? ' <span style="color:#1a472a;">•</span>' : ''}</div>`);
          }
        }
        function renderEvents(date) {
            const filtered = events.filter(ev => ev.date.toDateString() === date.toDateString());
            els.eventList.innerHTML = filtered.length === 0 ? '<div class="event-item"><p>No scheduled events for this day.</p></div>' : filtered.map(ev => `<div class="event-item"><h4>${ev.title} <span class="event-date">(${ev.date.toLocaleDateString()})</span></h4><p><strong>Location:</strong> ${ev.place}</p><p>${ev.description}</p></div>`).join('');
        }
        els.grid.addEventListener('click', e => { if (e.target.matches('.calendar-cell[data-date]')) { selectedDate = new Date(e.target.dataset.date); renderCalendar(); renderEvents(selectedDate); } });
        function changeMonth(offset) { currentDate.setMonth(currentDate.getMonth() + offset); selectedDate = null; renderCalendar(); if (els.prompt) els.eventList.innerHTML = els.prompt.outerHTML; }
        els.prevBtn.addEventListener('click', () => changeMonth(-1));
        els.nextBtn.addEventListener('click', () => changeMonth(1));
        renderCalendar();
    }
    
    window.fetchGeminiRecommendations = function() {
        const placeSelect = document.getElementById("user-place"), recommendationsDiv = document.getElementById("gemini-recommended-places");
        if (!placeSelect || !recommendationsDiv) return;
        const selectedOption = placeSelect.options[placeSelect.selectedIndex], lat = selectedOption.getAttribute('data-lat'), lon = selectedOption.getAttribute('data-lng');
        if (!lat || !lon) { alert("Please select your location for personalized recommendations."); return; }
        recommendationsDiv.innerHTML = `<div class="recommendation-loading"><div class="spinner-border text-success" role="status"></div><h5 class="mt-3">Finding perfect places for you...</h5></div>`;
        const params = new URLSearchParams({ latitude: lat, longitude: lon, user_place: selectedOption.value, place_type: document.getElementById("gemini-place-type").value, budget: document.getElementById("budget").value, duration: document.getElementById("duration").value, enhanced: 'true', context: 'andhra_pradesh' });
        fetch(`${geminiApiUrl}?${params.toString()}`).then(res => res.ok ? res.json() : Promise.reject(new Error(res.statusText))).then(data => { if (data.error) throw new Error(data.error); renderRecommendations(data); }).catch(err => { console.error('Error fetching recommendations:', err); recommendationsDiv.innerHTML = `<div class="alert alert-danger m-3">Sorry, could not fetch recommendations. Error: ${err.message}</div>`; });
    };
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
    window.clearRecommendations = function() {
        const div = document.getElementById("gemini-recommended-places"); if (div) div.innerHTML = `<div class="recommendation-placeholder text-center"><i class="fas fa-compass fa-3x text-muted mb-3"></i><h5>Ready to Discover?</h5><p>Select your preferences to get recommendations for Andhra Pradesh.</p></div>`;
    };
  
    // --- Itinerary Builder Logic ---
    function initializeItineraryPlanner() {
        const genBtn = document.getElementById('generateItineraryBtn');
        if (genBtn) genBtn.addEventListener('click', generateItinerary);
    }
    function generateItinerary() {
      const input = document.getElementById('startingPoint'); if (input.value === "") input.value = "Visakhapatnam";
      const container = document.getElementById('itineraryDays'), display = document.getElementById('generatedItinerary');
      if (!container || !display) return;
      display.classList.remove('d-none');
      container.innerHTML = `<div class="itinerary-loading-container"><div class="spinner-border text-success"></div><h5 class="loading-title mt-3">Crafting your Andhra Pradesh itinerary...</h5></div>`;
      setTimeout(() => {
        const places = window.PLACES_DATA || [];
        const plan = createSmartItinerary(parseInt(document.getElementById('tripDuration').value), document.getElementById('travelStyle').value, places);
        displayItinerary(plan, input.value, container);
      }, 1200);
    }
    function createSmartItinerary(duration, style, places) {
      const keywords = { adventure: ['adventure', 'park', 'hills', 'wildlife', 'beach'], cultural: ['temple', 'historical', 'museum', 'monument', 'cultural'], relaxation: ['beach', 'lake', 'park', 'garden', 'resort', 'hills'] };
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
      if (!plan || plan.length === 0) { container.innerHTML = '<p class="text-danger">Could not generate itinerary. Please try different options.</p>'; return; }
      let html = `<p class="text-muted">Starting from: <strong>${start}</strong></p>`;
      html += plan.map(d => `<div class="itinerary-day"><h6><i class="fas fa-calendar-day"></i> Day ${d.day}</h6>${d.places.map((p, i) => {
        const time = i === 0 ? "Morning" : (i === 1 ? "Afternoon" : "Evening");
        const name = p.name.replace(/'/g, "\\'");
        return `<div class="itinerary-place"><span class="place-time">${time}</span><div class="place-details"><strong>${p.name}</strong><small class="d-block text-muted">${p.category.charAt(0).toUpperCase() + p.category.slice(1)}</small></div><button class="btn btn-sm btn-outline-primary" onclick="showPlaceOnMap('${p.latitude}', '${p.longitude}', '${name}')" title="Show on Map"><i class="fas fa-map-marker-alt"></i></button></div>`;
      }).join('')}</div>`).join('');
      container.innerHTML = html;
    }
    window.resetItinerary = () => { document.getElementById('itineraryForm').reset(); document.getElementById('generatedItinerary').classList.add('d-none'); document.getElementById('itineraryDays').innerHTML = ''; };
    window.saveItinerary = () => { const toastEl = document.getElementById('itineraryToast'); if (toastEl) new bootstrap.Toast(toastEl).show(); };
    window.exportItinerary = () => alert('Export functionality is a work in progress!');
  
    // --- Review System ---
    function initializeReviewSystem() {
      const reviewForm = document.getElementById('addReviewForm');
      if (!reviewForm) return; // Exit if no form is found

      // Use only .star-rating inside the form to avoid conflicts
      const reviewStars = reviewForm.querySelectorAll('.star-rating');
      let selectedRating = 0;

      // 1. Star Rating UI Logic (robust, pointer events and accessibility)
      function updateStars(rating) {
          reviewStars.forEach(star => {
              const starValue = parseInt(star.dataset.rating);
              if (starValue <= rating) {
                  star.classList.remove('far');
                  star.classList.add('fas', 'text-warning', 'active');
                  star.style.color = '#ffd700';
              } else {
                  star.classList.remove('fas', 'text-warning', 'active');
                  star.classList.add('far');
                  star.style.color = '#dee2e6';
              }
          });
      }

      reviewStars.forEach(star => {
          star.tabIndex = 0; // Make focusable
          star.style.pointerEvents = 'auto'; // Ensure clickable
          star.setAttribute('role', 'button');
          star.setAttribute('aria-label', `Rate ${star.dataset.rating} stars`);
          // Click to set rating
          star.addEventListener('click', e => {
              e.preventDefault();
              selectedRating = parseInt(star.dataset.rating);
              updateStars(selectedRating);
          });
          // Keyboard accessibility
          star.addEventListener('keydown', e => {
              if (e.key === 'Enter' || e.key === ' ') {
                  selectedRating = parseInt(star.dataset.rating);
                  updateStars(selectedRating);
              }
          });
          // Hover preview
          star.addEventListener('mouseover', () => updateStars(parseInt(star.dataset.rating)));
      });
      // Mouse leaves the stars container
      const starsContainer = reviewForm.querySelector('.stars');
      if (starsContainer) {
          starsContainer.addEventListener('mouseleave', () => updateStars(selectedRating));
      }

      // 2. Form Submission Logic
      reviewForm.addEventListener('submit', function(e) {
          e.preventDefault();
          const placeId = document.getElementById('reviewPlace').value;
          const comment = document.getElementById('reviewComment').value;
          if (!placeId) {
              alert('Please select a place to review.');
              return;
          }
          if (selectedRating === 0) {
              alert('Please provide a rating by clicking on a star.');
              return;
          }
          if (!comment.trim()) {
              alert('Please write a comment for your review.');
              return;
          }
          submitReview(placeId, selectedRating, comment);
      });

      renderReviews();
    }
    function handleReviewSubmit(e) {
      e.preventDefault();
      const placeId = document.getElementById('reviewPlace').value, comment = document.getElementById('reviewComment').value;
      if (!placeId || !comment || selectedRating === 0) { alert('Please select a place, provide a rating, and write a comment.'); return; }
      submitReview(placeId, selectedRating, comment);
    }
    function submitReview(placeId, rating, comment) {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      fetch(window.ADD_REVIEW_URL.replace('0', placeId), {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrfToken, 'X-Requested-With': 'XMLHttpRequest' },
        body: `rating=${rating}&comment=${encodeURIComponent(comment)}`
      }).then(res => res.json()).then(data => { if (data.success) { alert('Review submitted!'); window.location.reload(); } else { alert(`Error: ${data.error}`); } }).catch(err => alert(`Error: ${err}`));
    }
    function renderReviews() {
        const container = document.getElementById('reviewsContainer'); if (!container) return;
        const places = window.PLACES_DATA || [];
        let totalReviews = 0, totalRating = 0;
        let html = '';
        places.forEach(place => {
            if (place.reviews && place.reviews.length > 0) {
                place.reviews.forEach(review => {
                    html += `
                    <div class="review-card mb-3">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <div class="reviewer-info">
                                <img src="https://ui-avatars.com/api/?name=${review.username}&background=1a472a&color=fff" class="reviewer-avatar" alt="">
                                <div><h6 class="mb-0">${review.username}</h6><small class="text-muted">${review.created_at}</small></div>
                            </div>
                            <div class="review-rating text-warning">${' <i class="fas fa-star"></i>'.repeat(review.rating)}${' <i class="far fa-star"></i>'.repeat(5-review.rating)}</div>
                        </div>
                        <div><h6 class="review-place">${place.name}</h6><p class="review-comment">${review.comment}</p></div>
                    </div>`;
                    totalReviews++; totalRating += review.rating;
                });
            }
        });
        if(totalReviews === 0) html = `<div class="text-center py-4"><i class="fas fa-comment-slash fa-3x text-muted mb-3"></i><p class="text-muted">No reviews yet for ${document.title.split(' - ')[0]}. Be the first to share your experience!</p></div>`;
        container.innerHTML = html;
        document.getElementById('totalReviewsCount').textContent = totalReviews;
        document.getElementById('averageRating').textContent = totalReviews > 0 ? (totalRating / totalReviews).toFixed(1) : '0.0';
    }

    // --- RUN INITIALIZATION ---
    initializePage();
  });
