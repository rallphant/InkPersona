from django.db import models
from django.conf import settings

class LiteraryCharacter(models.Model):
    """Represents a literary character from a book."""
    name = models.CharField(max_length=200)
    book = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(
        help_text="Detailed description of the character's personality, background, and speech patterns."
    )
    emoji = models.CharField(max_length=10, blank=True, help_text="Optional emoji representation.")
    tags = models.JSONField(default=list, help_text="List of keywords associated with the character.")
    image = models.ImageField(
        upload_to='character_images/',
        blank=True,
        null=True,
        help_text="Optional image for the character."
    )

    def __str__(self):
        """String representation of the character."""
        return f"{self.name} from {self.book}"

class Conversation(models.Model):
    """Represents a chat conversation between a user and a literary character."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    character = models.ForeignKey(
        LiteraryCharacter,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last message in the conversation."
    )

    class Meta:
        # Ensures only one conversation exists per user-character pair
        unique_together = ('user', 'character')
        # Orders conversations by most recently updated first by default
        ordering = ['-last_updated']

    def __str__(self):
        """String representation of the conversation."""
        # Use user's email for representation if available, otherwise username
        user_identifier = getattr(self.user, 'email', self.user.username)
        return f"Chat between {user_identifier} and {self.character.name}"

class ChatMessage(models.Model):
    """Represents a single message within a conversation."""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_text = models.TextField()
    is_user_message = models.BooleanField(
        default=True,
        help_text="True if the message is from the user, False if from the character/AI."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was created."
    )

    class Meta:
        # Orders messages chronologically within a conversation by default
        ordering = ['timestamp']

    def __str__(self):
        """String representation of the chat message."""
        sender = "User" if self.is_user_message else "Character"
        # Format timestamp for better readability if needed, otherwise default is fine
        # formatted_time = self.timestamp.strftime('%Y-%m-%d %H:%M')
        return f"{sender} message at {self.timestamp}"

