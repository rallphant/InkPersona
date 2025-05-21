import logging
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from groq import Groq, RateLimitError, APIError, APIConnectionError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LiteraryCharacter, Conversation, ChatMessage

logger = logging.getLogger(__name__)

# --- Instantiate Groq Client ---
# Attempts to initialize the Groq client using the GROQ_API_KEY environment variable.
try:
    groq_client = Groq()
    logger.info("Groq client initialized successfully.")
except APIError as e:
    logger.error(f"Failed to initialize Groq client (API Error): {e}", exc_info=True)
    groq_client = None # Set to None if initialization fails due to API issues (e.g., bad key format)
except Exception as e:
    # Catch other potential errors during initialization
    logger.error(f"Unexpected error initializing Groq client: {e}", exc_info=True)
    groq_client = None

# --- API Configuration ---
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")
MAX_HISTORY_MESSAGES = 50 # Number of previous messages to include in history
MAX_TOKENS_RESPONSE = 200
TEMPERATURE = 0.7

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_with_character(request):
    """
    Handles chat requests by sending the prompt and history to the Groq API
    and returning the character's response.
    """
    # Check if Groq client was initialized successfully
    if groq_client is None:
        logger.error("Groq client is not available. Cannot process chat request.")
        return Response(
            {'error': 'Chat service configuration error. Please contact support.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    try:
        data = request.data
        character_id = data.get('character_id')
        user_message_text = data.get('message')
        start_new = data.get('start_new', False)
        user = request.user

        if not character_id or not user_message_text:
            return Response(
                {'error': 'Missing required fields: character_id or message'},
                status=status.HTTP_400_BAD_REQUEST
            )

        character = get_object_or_404(LiteraryCharacter, pk=character_id)

        # Get or create the conversation object
        conversation, created = Conversation.objects.get_or_create(user=user, character=character)

        # Handle request to start a new conversation by deleting old messages
        if start_new and not created:
            logger.info(f"Starting new conversation for User: {user.email}, Character: {character.name}. Deleting old messages.")
            conversation.messages.all().delete()
            # Ensure 'created' reflects the state after potential deletion for history fetching
            created = True # Treat as created for history logic below

        # Save the user's current message *after* potential deletion
        ChatMessage.objects.create(
            conversation=conversation,
            message_text=user_message_text,
            is_user_message=True
        )

        # Prepare message history for the API prompt
        history_for_prompt = []
        if not created: # Only fetch history if it wasn't a newly created or cleared conversation
            # Fetch up to MAX_HISTORY_MESSAGES previous messages, excluding the one just saved
            history_messages = conversation.messages.order_by('-timestamp')[1:MAX_HISTORY_MESSAGES + 1]
            # Reverse to maintain chronological order for the prompt
            for msg in reversed(history_messages):
                role = "user" if msg.is_user_message else "assistant"
                history_for_prompt.append({"role": role, "content": msg.message_text})

        # Define the system prompt for the character persona
        system_message = f"""\
You are embodying the character {character.name} from the book "{character.book}" by {character.author}.
Your task is to speak, act, and think *only* as {character.name}, fully adopting their personality, speech patterns, knowledge, and mannerisms as described below. Do not break character. Do not act as an AI assistant.

Character Background: {character.description}

Respond concisely (1-2 paragraphs) based on this persona. If asked about events beyond the book's narrative, you may speculate based on the character's personality, but clarify that this is outside the original story."""

        # Construct the messages payload for the Groq API
        messages_for_api = [
            {"role": "system", "content": system_message},
            *history_for_prompt,
            {"role": "user", "content": user_message_text}
        ]

        ai_response_text = ""

        # Call the Groq API
        logger.info(f"Calling Groq API (model: {GROQ_MODEL}) for character {character_id} (User: {user.email})...")
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=messages_for_api,
                model=GROQ_MODEL,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS_RESPONSE,
            )
            # Extract the response content
            if chat_completion.choices:
                ai_response_text = chat_completion.choices[0].message.content.strip()
                logger.info(f"Groq API response received for character {character_id}")
            else:
                logger.warning(f"Groq API returned no choices for character {character_id}")
                ai_response_text = "[The character seems lost for words.]" # Fallback message

        # Handle specific Groq API errors
        except RateLimitError as e:
            logger.error(f"Groq Rate Limit Error: {e}", exc_info=True)
            return Response({'error': 'Chat service is busy. Please try again later.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except APIConnectionError as e:
            logger.error(f"Groq API Connection Error: {e}", exc_info=True)
            return Response({'error': 'Could not connect to the chat service. Please check your connection and try again.'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except APIError as e:
            logger.error(f"Groq API Error: {e}", exc_info=True)
            if hasattr(e, 'status_code') and e.status_code == 401:
                 return Response({'error': 'Chat service authentication failed. Please contact support.'}, status=status.HTTP_401_UNAUTHORIZED)
            error_message = getattr(e, 'message', str(e))
            return Response({'error': f'Chat service API error: {error_message}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # Handle any other unexpected errors during the API call
        except Exception as e:
            logger.error(f"Unexpected error during Groq API call: {e}", exc_info=True)
            return Response({'error': 'An unexpected error occurred while communicating with the chat service.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the AI's response to the database if received
        if ai_response_text:
            ChatMessage.objects.create(
                conversation=conversation,
                message_text=ai_response_text,
                is_user_message=False
            )
            logger.info(f"Saved AI response for character {character_id} (User: {user.email})")
        else:
             # Log if no text was generated or extracted
             logger.warning(f"No valid AI response text received or generated for character {character_id} (User: {user.email})")

        # Return the AI response to the frontend
        return Response({'response': ai_response_text}, status=status.HTTP_200_OK)

    # Handle errors before the API call (e.g., character not found)
    except LiteraryCharacter.DoesNotExist:
        logger.warning(f"Character not found for ID: {request.data.get('character_id')} requested by user {request.user.email}")
        return Response({'error': 'Character not found'}, status=status.HTTP_404_NOT_FOUND)
    # Catch any other unexpected errors during request processing
    except Exception as e:
        character_id_for_log = request.data.get('character_id', 'Unknown')
        logger.error(f"General error in chat processing for character ID {character_id_for_log} (User: {request.user.email}): {e}", exc_info=True)
        return Response({'error': 'An internal server error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

