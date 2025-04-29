from django.urls import path
from . import views
from . import api

app_name = 'characters'

urlpatterns = [
    path('', views.character_list, name='character_list'),
    path('<int:character_id>/', views.character_detail, name='character_detail'),
    path('history/', views.conversation_history, name='conversation_history'), # Add this line
    path('conversation/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('api/chat/', api.chat_with_character, name='chat_with_character'),
]
