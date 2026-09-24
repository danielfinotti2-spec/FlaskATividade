(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion) return;

    const elements = document.querySelectorAll(
        '.page-content > .d-flex, .page-content > h2, .page-content > section, .page-content > article, .page-content .card, .page-content .empty-state, .page-content .form-panel'
    );

    if (!('IntersectionObserver' in window)) return;

    elements.forEach((element, index) => {
        element.classList.add('motion-enter');
        if (element.classList.contains('card')) {
            element.style.setProperty('--motion-delay', `${Math.min(index % 4, 3) * 90}ms`);
        }
    });

    const observer = new IntersectionObserver((entries, currentObserver) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('motion-visible');
            currentObserver.unobserve(entry.target);
        });
    }, { threshold: 0.12 });

    elements.forEach((element) => observer.observe(element));
})();
