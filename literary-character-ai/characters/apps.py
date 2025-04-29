from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class CharactersConfig(AppConfig):
    """
    App configuration for the 'characters' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'characters'

    def ready(self):
        """
        Called once when Django starts.
        Currently skips local model loading as an external API (Groq) is used.
        """
        # Log that local model loading is skipped
        logger.info("Skipping local model loading (using Groq´s external API).")
        # No other startup actions needed here for now
        pass

