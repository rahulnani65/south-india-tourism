function addHotel() {
    const name = document.getElementById('hotelName').value;
    const placeName = document.getElementById('placeName').value;
    const address = document.getElementById('address').value;
    const amenities = document.getElementById('amenities').value;
    const distance = parseFloat(document.getElementById('distance').value);

    if (!name || !placeName || !address || !amenities || isNaN(distance)) {
        alert("Please fill all fields!");
        return;
    }

    fetch('/add-hotel/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            name: name,
            place: placeName,
            address: address,
            amenities: amenities,
            distance: distance,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Hotel added successfully!');
            document.getElementById('adminModal').querySelector('.btn-close').click();
            location.reload();
        } else {
            alert('Error adding hotel: ' + data.error);
        }
    })
    .catch(error => alert('Error: ' + error));
}

// Helper function to get CSRF token
function getCookie(name) {
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

// --- Weather, Recommendations, and UI Enhancements ---

document.addEventListener('DOMContentLoaded', function() {
    // Fetch weather data and suggestions
    fetchWeatherData();

    // Fetch personalized recommendations
    fetchRecommendations();

    // Smooth scrolling for in-page links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Back to Top button visibility
    const backToTopButton = document.querySelector('.back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });
    }
});

function fetchWeatherData() {
    fetch('/get-weather/')
        .then(response => response.json())
        .then(data => {
            const weatherWidget = document.getElementById('weather-widget');
            const suggestionsWidget = document.getElementById('weather-suggestions');

            if (weatherWidget && suggestionsWidget) {
                if (data.success) {
                    // Update weather widget
                    weatherWidget.innerHTML = `
                        <p><strong>Temperature:</strong> ${data.weather.temperature}°C</p>
                        <p><strong>Humidity:</strong> ${data.weather.humidity}%</p>
                        <p><strong>Condition:</strong> ${data.weather.condition}</p>
                    `;

                    // Update suggestions and safety tips
                    let suggestionsHTML = '<h5>Activity Suggestions</h5>';
                    data.suggestions.forEach(suggestion => {
                        suggestionsHTML += `<p>${suggestion}</p>`;
                    });
                    suggestionsHTML += '<h5 class="mt-3">Safety Tips</h5>';
                    data.safety_tips.forEach(tip => {
                        suggestionsHTML += `<p>${tip}</p>`;
                    });
                    suggestionsWidget.innerHTML = suggestionsHTML;
                } else {
                    weatherWidget.innerHTML = '<p>Unable to load weather data.</p>';
                    suggestionsWidget.innerHTML = '<p>No suggestions available.</p>';
                }
            }
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            const weatherWidget = document.getElementById('weather-widget');
            const suggestionsWidget = document.getElementById('weather-suggestions');
            if (weatherWidget) weatherWidget.innerHTML = '<p>Error loading weather data.</p>';
            if (suggestionsWidget) suggestionsWidget.innerHTML = '<p>Error loading suggestions.</p>';
        });
}

// Fetch personalized recommendations (placeholder)
document.addEventListener('DOMContentLoaded', function() {
  const recommendedPlacesDiv = document.getElementById('recommended-places');
  if (recommendedPlacesDiv) {
    // Simulate fetching recommendations (replace with actual API call)
    setTimeout(() => {
      recommendedPlacesDiv.innerHTML = `
        <div class="col-md-4 mb-4">
          <div class="card place-card h-100">
            <img src="{% static 'core/images/meenakshi-temple.jpg' %}" class="card-img-top" alt="Meenakshi Temple">
            <div class="card-body">
              <h5 class="card-title">Meenakshi Temple <span class="badge bg-secondary">religious</span></h5>
              <p class="card-text">A historic Hindu temple with towering gopurams, dedicated to Goddess Meenakshi.</p>
            </div>
          </div>
        </div>
      `;
    }, 2000);
  }

  // Back to Top Button Visibility
  const backToTopButton = document.querySelector('.back-to-top');
  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      backToTopButton.classList.add('visible');
    } else {
      backToTopButton.classList.remove('visible');
    }
  });
});
// Fetch personalized recommendations (placeholder)
document.addEventListener('DOMContentLoaded', function() {
    const recommendedPlacesDiv = document.getElementById('recommended-places');
    if (recommendedPlacesDiv) {
      // Simulate fetching recommendations (replace with actual API call)
      setTimeout(() => {
        recommendedPlacesDiv.innerHTML = `
          <div class="col-md-4 mb-4">
            <div class="card place-card h-100">
              <img src="{% static 'core/images/meenakshi-temple.jpg' %}" class="card-img-top" alt="Meenakshi Temple">
              <div class="card-body">
                <h5 class="card-title">Meenakshi Temple <span class="badge bg-secondary">religious</span></h5>
                <p class="card-text">A historic Hindu temple with towering gopurams, dedicated to Goddess Meenakshi.</p>
              </div>
            </div>
          </div>
        `;
      }, 2000);
    }
  
    // Back to Top Button Visibility
    const backToTopButton = document.querySelector('.back-to-top');
    window.addEventListener('scroll', function() {
      if (window.scrollY > 300) {
        backToTopButton.classList.add('visible');
      } else {
        backToTopButton.classList.remove('visible');
      }
    });
  });