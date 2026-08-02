document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('.nav-toggle');
    var links = document.getElementById('nav-links');
    if (!toggle || !links) return;

    var LABEL_OPEN = 'Abrir menú';
    var LABEL_CLOSE = 'Cerrar menú';

    function closeMenu() {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', LABEL_OPEN);
    }

    function openMenu() {
        links.classList.add('is-open');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.setAttribute('aria-label', LABEL_CLOSE);
    }

    toggle.addEventListener('click', function () {
        if (links.classList.contains('is-open')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    links.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape' || !links.classList.contains('is-open')) return;
        closeMenu();
        toggle.focus();
    });

    document.addEventListener('click', function (e) {
        if (!links.classList.contains('is-open')) return;
        if (links.contains(e.target) || toggle.contains(e.target)) return;
        closeMenu();
    });
});
