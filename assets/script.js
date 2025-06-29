// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Function to handle smooth scrolling
    function smoothScroll(event, targetId) {
        event.preventDefault();
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 70,
                behavior: 'smooth'
            });
            
            // Update URL hash without jumping
            history.pushState(null, null, '#' + targetId);
        }
    }
    
    // Add click handlers for all internal hash links
    function setupScrollHandlers() {
        // Handle all links that point to hash targets
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            if (link.getAttribute('href') !== '#') {
                link.addEventListener('click', function(e) {
                    const targetId = this.getAttribute('href').substring(1);
                    smoothScroll(e, targetId);
                });
            }
        });
        
        // Handle the Contact Me button specifically
        const contactBtn = document.querySelector('.contact-btn');
        if (contactBtn) {
            contactBtn.addEventListener('click', function(e) {
                smoothScroll(e, 'contact');
            });
        }
    }
    
    // Initial setup
    setupScrollHandlers();
    
    // Set up a MutationObserver to handle dynamically loaded content
    const observer = new MutationObserver(function(mutations) {
        setupScrollHandlers();
    });
    
    // Start observing the document with the configured parameters
    observer.observe(document.body, { childList: true, subtree: true });
}); 