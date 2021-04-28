from django.urls import path
from chat.api.views import ChatListView

urlpatterns = [
    path('messages/<int:sender>/<int:receiver>/', ChatListView.as_view({'get': 'list'})),
    path('messages/write/', ChatListView.as_view({'post': 'create'})),
]