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
  
    fetch('/add-hotel/', {  // Add a URL for a new view
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),  // Function to get CSRF token
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
        // Optionally, refresh the page or update the UI
        location.reload();
      } else {
        alert('Error adding hotel: ' + data.error);
      }
    })
    .catch(error => alert('Error: ' + error));
  
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
  }