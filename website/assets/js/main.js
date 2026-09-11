/**
 * LIGHTSPEED HOLDINGS LIMITED — INTERACTIVE SCRIPT
 */

document.addEventListener('DOMContentLoaded', () => {
  // Contact Form Submission Handler
  const contactForm = document.getElementById('briefing-form');
  const formSuccess = document.getElementById('form-success');

  if (contactForm && formSuccess) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      contactForm.style.display = 'none';
      formSuccess.style.display = 'block';
    });
  }

  // Smooth anchor scrolling
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#' || !targetId) return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({
          behavior: 'smooth',
        });
      }
    });
  });
});
