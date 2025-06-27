// Back to Top Button
const backToTopButton = document.querySelector('.back-to-top');

// Client-side filtering (optional, currently handled by server-side redirect)
document.addEventListener('DOMContentLoaded', function() {
  // Placeholder for additional state-specific JavaScript functionality
  console.log("State-specific JavaScript loaded.");
});

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

// Remove duplicate favorite button handling - this is handled by the partial template
// The partial template (favorite_button.html) already includes the necessary JavaScript