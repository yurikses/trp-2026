document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card) => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-2px)';
            card.style.transition = 'transform 0.15s ease';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'none';
        });
    });
});
