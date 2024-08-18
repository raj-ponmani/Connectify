# urls.py
from django.urls import path
from .views import UserListCreate, ConnectionRequestListCreateView, ConnectionRequestUpdateView, \
    ConnectedUsersListView, ChatMessageListView, UserCreate

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='get-users'),
    path('create-user/', UserCreate.as_view(), name='create-user'),
    path('connection-requests/', ConnectionRequestListCreateView.as_view(), name='connection-request-list-create'),
    path('connection-requests/<int:pk>/', ConnectionRequestUpdateView.as_view(), name='connection-request-update'),
    path('connected-users/', ConnectedUsersListView.as_view(), name='connected-users'),
    path('messages/<int:receiver_id>/', ChatMessageListView.as_view(), name='chat-message-list'),
]
