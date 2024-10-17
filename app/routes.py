# app/routes.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from .utils.search import generate_search_queries, search_videos, process_query
from .utils.analysis import analyze_videos
from .utils.suggestions import generate_suggestions
from config import Config
import concurrent.futures
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

MESSAGES = {
    'en': {
        'no_videos_to_analyze': "<p>No videos to analyze.</p>",
        'no_videos_after_filters': "<p>No videos match the applied filters.</p>",
        'no_search_queries_generated': "<p>No search queries were generated.</p>",
        'error_during_analysis': "<p>Error during analysis: {}</p>",
        'loading': "Loading...",
        'search_query_label': "Search Query:",
        'search_query_placeholder': "Enter your search...",
        'duration_label': "Duration:",
        'duration_options': {
            'any': "Any Duration",
            'short': "Less than 5 minutes",
            'medium': "5 to 20 minutes",
            'long': "20 minutes to 1 hour",
            'very_long': "More than 1 hour"
        },
        'min_publish_date_label': "Minimum Publish Date:",
        'optional': " (Optional)",
        'submit_button': "Search",
        'error_occurred': "<p>An error occurred during the search.</p>",
        'welcome_message': "Welcome to QualiTube! Use this tool to find relevant YouTube videos based on your interests. You can refine your searches using duration and publication date filters.",
        'optional_placeholder': "Optional",
        'clarification_message': "<p>Your query seems a bit general. Please provide a more specific search query.</p>",
    }
}

@main.route('/search_page', methods=['GET'])
def search_page():
    messages = MESSAGES['en']
    return render_template('index.html', messages=messages)

@main.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query', '').strip()
    duration_filter = request.form.get('duration_filter')
    min_publish_date = request.form.get('min_publish_date')

    messages = MESSAGES['en']

    if not search_query:
        logger.warning("Empty search query received.")
        return jsonify({'analysis': "<p>Please enter a search query.</p>", 'type': 'error'})

    logger.info(f"User query: '{search_query}'")

    # Générer des requêtes de recherche
    result = generate_search_queries(search_query)

    if result['type'] == 'error' or not result['content']:
        logger.warning("Error generating search queries or no queries generated.")
        return jsonify({'analysis': messages['clarification_message'], 'type': 'clarification_needed'})

    search_queries = result['content']

    # Traitement des requêtes de recherche
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=Config.MAX_WORKERS) as executor:
        future_to_query = {executor.submit(process_query, query): query for query in search_queries}
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Error processing query '{query}': {e}")

    logger.info(f"Extraction completed. Total number of results: {len(all_results)}")

    # Ajouter les filtres au formulaire de requête
    request.form = request.form.copy()
    if duration_filter:
        request.form['duration_filter'] = duration_filter
    if min_publish_date:
        request.form['min_publish_date'] = min_publish_date

    # Analyser les vidéos
    analysis = analyze_videos(all_results, search_query, messages=messages)

    return jsonify({'analysis': analysis, 'type': 'results'})

@main.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy-policy.html')

@main.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('main.search_page'))

@main.route('/suggest', methods=['POST'])
def suggest():
    partial_query = request.form.get('partial_query', '').strip()

    if not partial_query:
        return jsonify({'suggestions': []})

    # Générer des suggestions
    suggestions = generate_suggestions(partial_query)

    return jsonify({'suggestions': suggestions})
