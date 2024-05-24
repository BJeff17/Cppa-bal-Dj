document.addEventListener('DOMContentLoaded', function() {
    const categoryButtons = document.querySelectorAll('.category-button');

    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const categoryId = this.getAttribute('data-id');
            const candidatesContainer = document.querySelector(`.category-results[data-id="${categoryId}"] .candidates-container`);
            toggleResults(candidatesContainer);
        });
    });

    function toggleResults(container) {
        if (container.classList.contains('hidden')) {
            // Masquer les autres conteneurs de candidats
            const allContainers = document.querySelectorAll('.candidates-container');
            allContainers.forEach(item => {
                if (!item.classList.contains('hidden') && item !== container) {
                    item.classList.add('hidden');
                }
            });

            container.classList.remove('hidden');
            animateResults(container);
        } else {
            container.classList.add('hidden');
        }
    }

    function animateResults(container) {
        let candidates = Array.from(container.querySelectorAll('.candidate'));
        candidates.reverse(); // Afficher du 5ème au 1er
    
        let index = 0;
        const interval = setInterval(function() {
            if (index >= candidates.length) {
                clearInterval(interval);
                return;
            }
            candidates[index].classList.add('slide-in');
            index++;
        }, 800); // Intervalle de 800ms entre chaque affichage
    }
    
});
