from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import ConnectionRequest

User = get_user_model()

class UserFunctionalityTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.user3 = User.objects.create_user(username='user3', password='pass1234')

    def test_user_authentication_and_list(self):
        # Authenticate as user1
        self.client.force_authenticate(user=self.user1)

        url = reverse('get-users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_data = response.data['users']

        # Check that user1 is excluded from the list
        self.assertNotIn(self.user1.id, [user['id'] for user in users_data])

        # Check that user2 and user3 are in the list (since no connections are made yet)
        self.assertIn(self.user2.id, [user['id'] for user in users_data])
        self.assertIn(self.user3.id, [user['id'] for user in users_data])

    def test_send_connection_request(self):
        # Authenticate as user1
        self.client.force_authenticate(user=self.user1)

        url = reverse('connection-request-list-create')
        response = self.client.post(url, {'connection_receiver': self.user2.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ConnectionRequest.objects.filter(connection_sender=self.user1, connection_receiver=self.user2).exists())

    def test_accept_connection_request(self):
        # Create a connection request from user1 to user2
        connection_request = ConnectionRequest.objects.create(
            connection_sender=self.user1, connection_receiver=self.user2, status='pending'
        )

        # Authenticate as user2 (the receiver)
        self.client.force_authenticate(user=self.user2)

        url = reverse('connection-request-update', kwargs={'pk': connection_request.id})
        response = self.client.patch(url, {'status': 'accepted'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        connection_request.refresh_from_db()
        self.assertEqual(connection_request.status, 'accepted')

    def test_reject_connection_request(self):
        # Create a connection request from user1 to user2
        connection_request = ConnectionRequest.objects.create(
            connection_sender=self.user1, connection_receiver=self.user2, status='pending'
        )

        # Authenticate as user2 (the receiver)
        self.client.force_authenticate(user=self.user2)

        url = reverse('connection-request-update', kwargs={'pk': connection_request.id})
        response = self.client.patch(url, {'status': 'rejected'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        connection_request.refresh_from_db()
        self.assertEqual(connection_request.status, 'rejected')
