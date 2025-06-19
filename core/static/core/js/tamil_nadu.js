// tamil_nadu.js - All Tamil Nadu page-specific JS logic
(function() {
  // --- Review System ---
  let selectedRating = 0;
  document.addEventListener('DOMContentLoaded', function() {
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
  // --- Itinerary, Gemini, Map, and other Tamil Nadu logic ---
  // (Move all other page-specific JS here, using window.* for functions called from HTML)
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
  // ... existing code ...
  // In your fetchGeminiRecommendations, after fetching data:
  // renderGeminiRecommendations(uniquePlaces, weatherData);
})(); 