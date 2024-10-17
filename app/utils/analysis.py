# app/utils/analysis.py
from config import Config
import logging
import re
from bs4 import BeautifulSoup
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configurer Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

def get_messages():
    return {
        'no_videos_to_analyze': "<p>No videos to analyze.</p>",
        'no_videos_after_filters': "<p>No videos match the applied filters.</p>",
        'error_during_analysis': "<p>Error during analysis: {}</p>",
        'clarification_message': "<p>Your query seems a bit general. Please provide a more specific search query.</p>",
    }

def analyze_videos(videos, user_query, messages=None):
    if not messages:
        messages = get_messages()

    if not videos:
        logger.info("No videos to analyze.")
        return messages['no_videos_to_analyze']

    videos_to_analyze = [video for video in videos if video['status'] == 'data_extracted']
    logger.info(f"Videos with extracted data: {len(videos_to_analyze)}")

    if not videos_to_analyze:
        logger.info("No videos with available data for analysis.")
        return messages['no_videos_to_analyze']

    # Appliquer les filtres de durée et de date de publication
    duration_filter = None  # Récupéré depuis la requête dans routes.py
    min_publish_date = None  # Récupéré depuis la requête dans routes.py

    # Note : Les filtres sont déjà appliqués dans routes.py via `request.form`

    # Filtrage par durée
    duration_filter = None  # Vous devrez passer ces valeurs depuis routes.py
    min_publish_date = None

    # Pour l'exemple, supposons que ces filtres sont passés comme arguments
    # Vous pouvez modifier la fonction pour accepter ces paramètres si nécessaire

    # Filtrage par durée
    duration_filter = None  # Placeholder, à implémenter si nécessaire
    min_publish_date = None  # Placeholder, à implémenter si nécessaire

    # ... (Vous pouvez ajouter le filtrage ici si nécessaire)

    # Deduplication des vidéos par ID
    unique_videos = {video['video_id']: video for video in videos_to_analyze}
    videos_to_analyze = list(unique_videos.values())
    logger.info(f"Number of videos after deduplication: {len(videos_to_analyze)}")

    # Limiter le nombre de vidéos à analyser pour éviter les prompts trop longs
    videos_to_analyze = videos_to_analyze[:Config.MAX_VIDEOS_TO_ANALYZE]
    logger.info(f"Analyzing top {Config.MAX_VIDEOS_TO_ANALYZE} videos.")

    # Préparer le prompt pour l'analyse (sans résumé)
    prompt_template = (
        f"You are helping a user find the best YouTube videos matching their query: \"{user_query}\". "
        "For each of the following videos, do the following: "
        "1. Analyze the video's content based on its title, description, and transcript, and provide a concise explanation addressing the user directly, explaining why this video is particularly useful for them. "
        "2. Assign a relevance score from 1 to 10 indicating how well the video matches the user's query. "
        "Present the information in an HTML block structured as follows: "
        "<div class='video-result'>"
        "<img src='[Thumbnail URL]' alt='Video Thumbnail'>"
        "<div class='video-details'>"
        "<h2>[Video Title]</h2>"
        "<p><strong>Duration:</strong> [Duration in hours, minutes, and seconds]</p>"
        "<p><strong>Publication Date:</strong> [Publication date]</p>"
        "<p><strong>Relevance Score:</strong> [Score]</p>"
        "<p><strong>Why this video is for you:</strong> [Personalized explanation]</p>"
        "<a href='https://www.youtube.com/watch?v=[Video ID]' target='_blank'>Watch Video</a>"
        "</div>"
        "</div>"
        "Only include the HTML code without any additional text."
    )
    video_data_header = "Video data:"

    # Diviser les vidéos en lots pour éviter de dépasser les limites du modèle
    video_batches = [videos_to_analyze[i:i + Config.BATCH_SIZE] for i in range(0, len(videos_to_analyze), Config.BATCH_SIZE)]

    analyses = []

    for batch in video_batches:
        # Préparer les données des vidéos pour le prompt
        video_data = ""
        for video in batch:
            hours, remainder = divmod(video['length'], 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_parts = []
            if hours > 0:
                duration_parts.append(f"{hours}h")
            if minutes > 0:
                duration_parts.append(f"{minutes}m")
            if seconds > 0 or not duration_parts:
                duration_parts.append(f"{seconds}s")
            duration_str = ' '.join(duration_parts)
            transcript_snippet = video['transcript'][:Config.MAX_SUBTITLE_LENGTH]  # Limiter la longueur de la transcription
            video_data += (
                f"ID: {video['video_id']}\n"
                f"Title: {video['title']}\n"
                f"Description: {video['description']}\n"
                f"Duration: {duration_str}\n"
                f"Publication Date: {video['publish_date']}\n"
                f"Thumbnail URL: {video['thumbnail_url']}\n"
                f"Transcript: {transcript_snippet}\n\n"
            )

        full_prompt = f"{prompt_template}\n\n{video_data_header}\n{video_data}"

        logger.info("Sending prompt to Gemini API for analysis.")
        # Envoyer le prompt à l'API Gemini
        try:
            response = model.generate_content(full_prompt)
            if response:
                analysis = response.text.strip()
                # Supprimer les fences de code HTML potentiels
                analysis = re.sub(r'^```html\s*', '', analysis, flags=re.MULTILINE)
                analysis = re.sub(r'\s*```$', '', analysis, flags=re.MULTILINE)
                analyses.append(analysis)
            else:
                logger.error("No response from the model.")
        except Exception as e:
            logger.error(f"Error communicating with Gemini API: {e}")
            return messages['error_during_analysis'].format(str(e))

    # Combiner toutes les analyses
    combined_analysis = "\n".join(analyses)

    # Trier les vidéos par score de pertinence
    try:
        # Parser le HTML combiné pour extraire les blocs vidéo individuels
        soup = BeautifulSoup(combined_analysis, 'html.parser')
        video_blocks = soup.find_all('div', class_='video-result')

        # Liste pour stocker les tuples de (score, bloc HTML)
        scored_videos = []

        for block in video_blocks:
            # Extraire le score de pertinence
            score_tag = block.find('p', string=re.compile(r'Relevance Score:\s*\d+'))
            if score_tag:
                score_text = score_tag.get_text()
                match = re.search(r'Relevance Score:\s*(\d+)', score_text)
                if match:
                    score = int(match.group(1))
                else:
                    score = 0
            else:
                score = 0
            # Ajouter à la liste
            scored_videos.append((score, str(block)))

        # Trier les vidéos par score de pertinence décroissant
        scored_videos.sort(reverse=True, key=lambda x: x[0])

        # Reconstruire le HTML final trié
        sorted_html = "\n".join([block_html for score, block_html in scored_videos])

        logger.info("Video analysis and sorting successful.")
        return sorted_html

    except Exception as e:
        logger.error(f"Error processing analysis results: {e}")
        return messages['error_during_analysis'].format(str(e))
