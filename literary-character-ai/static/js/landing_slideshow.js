document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with class 'slide' within an element with class 'slideshow'
    const slides = document.querySelectorAll('.slideshow .slide');
    let currentSlide = 0;
    const slideInterval = 5000; // Time between slides in milliseconds (5 seconds)
    let intervalId = null; // Variable to store the interval timer ID

    /**
     * Shows the slide at the specified index by adding the 'active' class
     * and removing it from all other slides.
     * @param {number} index - The index of the slide to show.
     */
    function showSlide(index) {
        slides.forEach((slide, i) => {
            // Use classList.toggle for potentially slightly cleaner adding/removing
            slide.classList.toggle('active', i === index);
        });
    }

    /**
     * Calculates the next slide index and calls showSlide.
     */
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length; // Cycle through slides
        showSlide(currentSlide);
    }

    // Only proceed if there are slides found
    if (slides.length > 1) {
        // Show the first slide initially
        showSlide(currentSlide);
        // Start cycling through slides at the specified interval
        intervalId = setInterval(nextSlide, slideInterval);
    } else if (slides.length === 1) {
         // If there's only one slide, just ensure it's visible
         showSlide(0);
    } else {
        console.warn("Slideshow elements not found or only one slide present. Interval not started.");
    }

   
});
