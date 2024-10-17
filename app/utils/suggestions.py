# app/utils/suggestions.py
import google.generativeai as genai
import logging
from config import Config

logger = logging.getLogger(__name__)

# Configurer Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-8b")

def generate_suggestions(partial_query, num_suggestions=5):
    prompt = (
        f"Based on the partial input: \"{partial_query}\", generate up to {num_suggestions} relevant and concise search suggestions that the user might be typing. "
        "Each suggestion should be a continuation or refinement of the partial input, suitable for searching on YouTube. "
        "Provide each suggestion on a separate line without numbering or additional text."
    )
    try:
        logger.info("Generating search suggestions with Gemini API.")
        response = model.generate_content(prompt)
        generated_text = response.text.strip()

        # Extraire les suggestions
        suggestions = [line.strip() for line in generated_text.split('\n') if line.strip()]
        logger.info(f"Generated suggestions: {suggestions}")
        return suggestions[:num_suggestions]
    except Exception as e:
        logger.error(f"Error generating suggestions: {e}")
        return []
