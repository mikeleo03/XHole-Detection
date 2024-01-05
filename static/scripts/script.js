// script.js
document.addEventListener('DOMContentLoaded', function () {
    var overlay = document.getElementById('overlay');
    var checkbox = document.getElementById('check');

    checkbox.addEventListener('change', function () {
        overlay.style.transition = 'opacity 0.7s';
        overlay.style.opacity = this.checked ? 1 : 0;
        overlay.style.display = this.checked ? 'block' : 'none';
    });
});
