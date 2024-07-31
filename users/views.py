from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response

from .models import ConnectionRequest, ChatMessage, CustomUser
from .serializers import UserSerializer, ConnectionRequest, ConnectionRequestSerializer, ChatMessageSerializer, \
    CurrentUserSerializer

User = get_user_model()


class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user

        # Get the list of users who sent a request to the current user or the users to whom the current user sent a request
        users_with_requests = CustomUser.objects.filter(
            Q(connection_sender__connection_receiver=current_user,
              connection_sender__status__in=['pending', 'accepted']) |
            Q(connection_receiver__connection_sender=current_user,
              connection_receiver__status__in=['pending', 'accepted'])
        ).values_list('pk', flat=True).distinct()

        print(users_with_requests)

        # Exclude the current user and connected users from the queryset
        return User.objects.exclude(id=self.request.user.id).exclude(id__in=users_with_requests)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        current_user_serializer = CurrentUserSerializer(request.user)
        return Response({
            'users': serializer.data,
            'current_user': current_user_serializer.data
        })


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ConnectionRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer

    def get_queryset(self):
        return ConnectionRequest.objects.filter(connection_receiver=self.request.user, status='pending')

    def perform_create(self, serializer):
        connection_receiver_id = self.request.data.get('connection_receiver')
        try:
            connection_receiver = CustomUser.objects.get(id=connection_receiver_id)
        except CustomUser.DoesNotExist:
            raise serializer.ValidationError("The specified user does not exist.")

        serializer.save(connection_sender=self.request.user, connection_receiver=connection_receiver)


class ConnectionRequestUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer
    queryset = ConnectionRequest.objects.all()


class ChatMessageListView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        receiver_id = self.kwargs['receiver_id']
        return ChatMessage.objects.filter(
            sender=self.request.user,
            receiver_id=receiver_id
        ) | ChatMessage.objects.filter(
            sender_id=receiver_id,
            receiver=self.request.user
        )

    def perform_create(self, serializer):
        receiver = self.request.data.get('receiver')
        print(receiver)
        try:
            receiver = CustomUser.objects.get(id=receiver)
        except CustomUser.DoesNotExist:
            raise serializer.ValidationError("The specified user does not exist.")
        serializer.save(sender=self.request.user, receiver=receiver)


class ConnectedUsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accepted_requests = ConnectionRequest.objects.filter(status='accepted').filter(
            Q(connection_sender=user) | Q(connection_receiver=user))

        connected_users = set()
        for request in accepted_requests:
            if request.connection_sender != user:
                connected_users.add(request.connection_sender)
            if request.connection_receiver != user:
                connected_users.add(request.connection_receiver)

        return connected_users

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
