// script.js
document.addEventListener('DOMContentLoaded', function () {
    var overlay = document.getElementById('overlay');
    var checkbox = document.getElementById('check');

    function closeMenu() {
        overlay.style.transition = 'opacity 0.7s';
        overlay.style.opacity = 0;
        checkbox.checked = false;
        overlay.classList.remove('active');
    }

    checkbox.addEventListener('change', function () {
        overlay.style.transition = 'opacity 0.7s';
        overlay.style.opacity = this.checked ? 1 : 0;
        overlay.classList.toggle('active', this.checked);
        overlay.style.display = this.checked ? 'block' : 'none';
    });

    // Close the menu when tapping outside the navigation area
    overlay.addEventListener('click', closeMenu);
});

// script.js
document.addEventListener('DOMContentLoaded', function () {
    var animatedSections = document.querySelectorAll('.animated-section');

    function isElementInViewport(el) {
        var rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function handleScroll() {
        var scrolledToTop = window.scrollY === 0;

        animatedSections.forEach(function (animatedSection) {
            var isInViewport = isElementInViewport(animatedSection);

            if (isInViewport && !animatedSection.classList.contains('active')) {
                animatedSection.classList.add('active');
            } else if (!isInViewport && animatedSection.classList.contains('active') && !scrolledToTop) {
                animatedSection.classList.remove('active');
            }
        });

        // Optionally, remove the event listener to avoid unnecessary checks
        if (document.querySelectorAll('.animated-section:not(.active)').length === 0) {
            window.removeEventListener('scroll', handleScroll);
        }
    }

    // Initial check on page load
    handleScroll();

    // Check on scroll
    window.addEventListener('scroll', handleScroll);
});
