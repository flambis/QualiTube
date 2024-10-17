// app/static/js/scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');
    const searchQueryInput = document.getElementById('search_query');

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(searchForm);
        const data = {
            search_query: formData.get('search_query'),
            duration_filter: formData.get('duration_filter'),
            min_publish_date: formData.get('min_publish_date')
        };

        resultsDiv.innerHTML = `<p>Loading...</p>`;

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(data)
            });

            const result = await response.json();

            if (result.type === 'results') {
                resultsDiv.innerHTML = result.analysis;
            } else if (result.type === 'error') {
                resultsDiv.innerHTML = result.analysis;
            } else if (result.type === 'clarification_needed') {
                resultsDiv.innerHTML = result.analysis;
            }
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = `<p>An error occurred during the search.</p>`;
        }
    });

    // Gestion des suggestions de recherche
    searchQueryInput.addEventListener('input', async () => {
        const partialQuery = searchQueryInput.value.trim();
        if (partialQuery.length === 0) {
            // Afficher ou masquer les suggestions selon votre implémentation
            return;
        }

        try {
            const response = await fetch('/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ partial_query: partialQuery })
            });

            const result = await response.json();
            console.log('Suggestions:', result.suggestions);
            // Implémentez l'affichage des suggestions selon vos besoins
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        }
    });
});
