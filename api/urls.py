from django.urls import path
from .views import GenerateCaseView, ChatMessageView, ClearChatHistoryView

urlpatterns = [
    path('generate-case', GenerateCaseView.as_view(), name='generate_case'),
    path('chat/messages', ChatMessageView.as_view(), name='chat_messages'),
    path('clear-chat-history', ClearChatHistoryView.as_view(), name='clear_chat_history'),
]