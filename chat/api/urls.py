from django.urls import path
from chat.api.views import MessageView, ChatView

urlpatterns = [
    path('messages/<int:sender>/<int:receiver>/', MessageView.as_view({'get': 'list'})),
    path('messages/write/', MessageView.as_view({'post': 'create'})),
    path('', ChatView.as_view({'get': 'list'}), name='chat'),
    # path('chat/<int:sender>/<int:receiver>/', ChatView.as_view({'get': 'retrieve'})),
]