from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  
        self.login_url = reverse('login')      
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password1"
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data['data'])

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'].lower() or response.data['data'])

    def test_user_registration_password_validation(self):
        invalid_data = self.user_data.copy()
        invalid_data['password'] = 'pass'  # too short and no capital
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', str(response.data['message']).lower())

    def test_user_login_success(self):
        User.objects.create_user(**self.user_data)
        login_data = {"username": self.user_data['username'], "password": self.user_data['password']}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])

    def test_user_login_fail_wrong_credentials(self):
        login_data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
