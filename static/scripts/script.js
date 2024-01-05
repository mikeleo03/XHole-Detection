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
