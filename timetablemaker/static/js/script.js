/* script.js */

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('header nav a');
    const currentUrl = window.location.href;

    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.style.fontWeight = 'bold';
            link.style.color = 'lightblue';
        }
    });
});