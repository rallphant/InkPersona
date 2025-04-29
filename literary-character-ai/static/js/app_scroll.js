document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('.app-header');
    const mainElement = document.querySelector('main'); // Scrollable main content area
    const sections = document.querySelectorAll('main .section'); // Sections within main
    const body = document.querySelector('.app-body'); // Used for potential global classes

    // --- Shrink Header on Scroll Logic ---
    if (header && mainElement) {
        const handleHeaderScroll = () => {
            // Add 'scrolled' class to header if main content is scrolled down
            if (mainElement.scrollTop > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        };
        // Listen to scroll events on the main element
        mainElement.addEventListener('scroll', handleHeaderScroll, { passive: true });
        handleHeaderScroll(); // Run once on load to set initial state
    } else {
        console.warn("Header or Main element not found for scroll effects.");
    }

    // --- Section Activation on Scroll Logic ---
    if (sections.length > 0 && mainElement) {
        let currentlyActiveSection = null; // Track the currently visible section

        const sectionOptions = {
            root: mainElement, // Observe intersections within the main scrollable area
            threshold: 0.5 // Trigger when 50% of the section is visible
        };

        const sectionObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                // Check if the section is intersecting enough to be considered active
                if (entry.isIntersecting && entry.intersectionRatio >= sectionOptions.threshold) {
                    // Activate the new section if it's not already the active one
                    if (entry.target !== currentlyActiveSection) {
                        // Deactivate the previously active section, if any
                        if (currentlyActiveSection) {
                            currentlyActiveSection.classList.remove('active');
                        }
                        // Activate the current section
                        entry.target.classList.add('active');
                        currentlyActiveSection = entry.target;
                    }
                } else {
                    // Deactivate the section if it's no longer intersecting enough
                    // and it was the currently active one
                    if (entry.target === currentlyActiveSection) {
                        entry.target.classList.remove('active');
                        currentlyActiveSection = null;
                    }
                }
            });
        }, sectionOptions);

        // Observe all sections found
        sections.forEach(section => sectionObserver.observe(section));

        // --- Initial Activation Check ---
        // Sometimes the first section might already be in view on load.
        // Use a small delay to ensure layout is stable.
        setTimeout(() => {
            if (sections.length > 0 && !sections[0].classList.contains('active')) {
                const firstSectionRect = sections[0].getBoundingClientRect();
                const mainRect = mainElement.getBoundingClientRect();
                // Check if the top of the first section is at or near the top of the main container
                if (firstSectionRect.top <= mainRect.top + 5) {
                    sections[0].classList.add('active');
                    currentlyActiveSection = sections[0];
                }
            }
        }, 150);

    } else {
        // Log if no sections were found or main element is missing
        console.log("No sections found for observation or main element missing.");
    }
});
