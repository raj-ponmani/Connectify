from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import ConnectionRequest, ChatMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source='connection_sender', read_only=True)
    receiver = UserSerializer(source='connection_receiver', read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = ['id', 'status', 'created_at', 'sender', 'receiver']

    def create(self, validated_data):
        sender = validated_data.get('connection_sender')
        receiver = validated_data.get('connection_receiver')

        # Use get_or_create to avoid duplicate connection requests
        connection_request, created = ConnectionRequest.objects.get_or_create(
            connection_sender=sender,
            connection_receiver=receiver,
            defaults={'status': 'pending'}  # Set default status if request is created
        )

        return connection_request


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
