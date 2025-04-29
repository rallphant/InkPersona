document.addEventListener('DOMContentLoaded', () => {
    const scrollContainer = document.querySelector('.scroll-container');
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const revealedSection = document.querySelector('.revealed-section');
    const body = document.querySelector('.landing-body');

    // Basic check for essential elements
    if (!scrollContainer || !scrollIndicator || !revealedSection || !body) {
        console.warn("Required elements for landing page scroll effects not found.");
        return; // Exit if elements aren't found
    }

    // --- Hide/Show Scroll Indicator Logic ---
    let indicatorHidden = false;
    const handleScrollIndicator = () => {
        const shouldHide = scrollContainer.scrollTop > 50;
        if (shouldHide && !indicatorHidden) {
            scrollIndicator.classList.add('hidden');
            indicatorHidden = true;
        } else if (!shouldHide && indicatorHidden) {
            scrollIndicator.classList.remove('hidden');
            indicatorHidden = false;
        }
    };
    // Attach listener to the scroll container
    scrollContainer.addEventListener('scroll', handleScrollIndicator, { passive: true });
    // Run on load in case page loads scrolled
    handleScrollIndicator();


    // --- Detect Revealed Section Visibility Logic ---
    const observerOptions = {
        root: scrollContainer, // Observe intersections within the scroll container
        threshold: 0.6 // Trigger when 60% of the section is visible
    };

    const intersectionCallback = (entries, observer) => {
        // Since we only observe one entry, we can access it directly
        const entry = entries[0];

        // Check if it's intersecting enough to be considered 'active'
        if (entry.isIntersecting && entry.intersectionRatio >= observerOptions.threshold) {
            // Add class only if it's not already present
            if (!body.classList.contains('revealed-active')) {
                body.classList.add('revealed-active');
            }
        } else {
            // Remove class only if it is present
            if (body.classList.contains('revealed-active')) {
                body.classList.remove('revealed-active');
            }
        }
    };

    const observer = new IntersectionObserver(intersectionCallback, observerOptions);

    // Start observing the revealed section
    observer.observe(revealedSection);

});
