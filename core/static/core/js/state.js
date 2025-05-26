// Back to Top Button
const backToTopButton = document.querySelector('.back-to-top');

window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    backToTopButton.classList.add('visible');
  } else {
    backToTopButton.classList.remove('visible');
  }
});

backToTopButton.addEventListener('click', (e) => {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

// Active Navigation Link
const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.secondary-nav .nav-link');

window.addEventListener('scroll', () => {
  let current = '';
  
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    
    if (window.scrollY >= (sectionTop - 200)) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href').substring(1) === current) {
      link.classList.add('active');
    }
  });
});

// Smooth Scroll for Navigation
document.querySelectorAll('.secondary-nav .nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const targetId = link.getAttribute('href').substring(1);
    const targetSection = document.getElementById(targetId);
    
    if (targetSection) {
      targetSection.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});

// Favorite Button Handling
document.addEventListener('DOMContentLoaded', function() {
  // Handle state favorite button
  const stateFavoriteForm = document.querySelector('form[action*="state_favorite"]');
  if (stateFavoriteForm) {
    stateFavoriteForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const button = this.querySelector('button');
      const isFavorited = button.classList.contains('btn-danger');
      
      // Show loading state
      button.disabled = true;
      button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
      
      // Submit the form
      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: {
          'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          // Update button state
          if (isFavorited) {
            button.className = 'btn btn-outline-light btn-sm mt-2';
            button.innerHTML = '<i class="far fa-heart"></i> Add to Favorites';
          } else {
            button.className = 'btn btn-danger btn-sm mt-2';
            button.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
          }
          // Update the form action for the next click
          const newAction = isFavorited ? 
            this.action.replace('remove_state_favorite', 'add_state_favorite') :
            this.action.replace('add_state_favorite', 'remove_state_favorite');
          this.action = newAction;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        // Reset button state on error
        button.disabled = false;
        if (isFavorited) {
          button.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
        } else {
          button.innerHTML = '<i class="far fa-heart"></i> Add to Favorites';
        }
      })
      .finally(() => {
        button.disabled = false;
      });
    });
  }

  // Handle place favorite buttons
  const placeFavoriteForms = document.querySelectorAll('form[action*="favorite"]');
  placeFavoriteForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const button = this.querySelector('button');
      const isFavorited = button.classList.contains('btn-danger');
      
      // Show loading state
      button.disabled = true;
      button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
      
      // Submit the form
      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: {
          'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          // Update button state
          if (isFavorited) {
            button.className = 'btn btn-outline-primary btn-sm mt-2';
            button.innerHTML = '<i class="far fa-heart"></i> Add to Favorites';
          } else {
            button.className = 'btn btn-danger btn-sm mt-2';
            button.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
          }
          // Update the form action for the next click
          const newAction = isFavorited ? 
            this.action.replace('remove_favorite', 'add_favorite') :
            this.action.replace('add_favorite', 'remove_favorite');
          this.action = newAction;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        // Reset button state on error
        button.disabled = false;
        if (isFavorited) {
          button.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
        } else {
          button.innerHTML = '<i class="far fa-heart"></i> Add to Favorites';
        }
      })
      .finally(() => {
        button.disabled = false;
      });
    });
  });
});