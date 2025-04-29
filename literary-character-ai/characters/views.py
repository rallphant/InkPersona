from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import LiteraryCharacter, Conversation
from .forms import CustomUserCreationForm


def landing_page(request):
    """Displays the landing page with a selection of characters."""
    characters_with_images = LiteraryCharacter.objects.exclude(image__isnull=True).exclude(image__exact='')
    return render(request, 'landing_page.html', {'characters': characters_with_images})

def character_list(request):
    """Displays a list of all available characters."""
    characters = LiteraryCharacter.objects.all()
    return render(request, 'characters/character_list.html', {'characters': characters})

@login_required
def character_detail(request, character_id):
    """Displays the chat interface for a specific character, loading history if available."""
    character = get_object_or_404(LiteraryCharacter, pk=character_id)
    message_history = []
    is_new_conversation = request.GET.get('new') == 'true'

    if not is_new_conversation:
        try:
            # Attempt to load existing conversation history
            conversation = Conversation.objects.get(user=request.user, character=character)
            message_history = conversation.messages.all().order_by('timestamp')
        except Conversation.DoesNotExist:
            # No previous conversation exists, history remains empty
            pass

    context = {
        'character': character,
        'message_history': message_history,
        'is_new_conversation': is_new_conversation,
    }
    return render(request, 'characters/character_detail.html', context)

def about(request):
    """Displays the about page."""
    return render(request, 'about.html')

def signup(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in using the custom email backend
            login(request, user, backend='characters.backends.EmailBackend')
            return redirect('characters:character_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def conversation_history(request):
    """Displays a list of the user's past conversations."""
    user_conversations = Conversation.objects.filter(user=request.user).order_by('-last_updated')
    context = {
        'conversations': user_conversations,
    }
    return render(request, 'characters/conversation_history.html', context)

@require_POST # Ensures this view only accepts POST requests
@login_required
def delete_conversation(request, conversation_id):
    """Deletes a specific conversation belonging to the user."""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    # Deleting the conversation cascades and deletes related ChatMessages
    conversation.delete()
    return redirect(reverse('characters:conversation_history'))

class CustomLogoutView(BaseLogoutView):
    """Customizes the logout view to display characters on the logged-out page."""
    template_name = 'registration/logged_out.html'
    # next_page = None ensures the template is shown instead of immediate redirect
    next_page = None

    def get_context_data(self, **kwargs):
        """Adds character data to the context for the logout page slideshow."""
        context = super().get_context_data(**kwargs)
        # Fetch a few random characters with images for the animation
        context['characters'] = LiteraryCharacter.objects.filter(image__isnull=False).order_by('?')[:4]
        return context
