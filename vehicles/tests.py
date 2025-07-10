from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Vehicle

class VehicleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Testpass123")
        self.client.login(username="testuser", password="Testpass123")
        self.vehicle_data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2020,
            "plate": "ABC-123"
        }

    def authenticate(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "Testpass123"
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['data']['access'])

    def test_create_vehicle(self):
        self.authenticate()
        response = self.client.post(reverse('vehicle-list-create'), self.vehicle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 1)
        self.assertEqual(response.data['message'], "Vehicle created successfully")

    def test_list_vehicles(self):
        self.authenticate()
        self.client.post(reverse('vehicle-list-create'), self.vehicle_data, format='json')
        response = self.client.get(reverse('vehicle-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 1)
        self.assertTrue(len(response.data['data']) > 0)

    def test_vehicle_detail_update(self):
        self.authenticate()
        response = self.client.post(reverse('vehicle-list-create'), self.vehicle_data, format='json')
        vehicle_id = response.data['data']['id']
        updated_data = {**self.vehicle_data, "model": "City"}
        response = self.client.put(reverse('vehicle-detail', args=[vehicle_id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['model'], "City")

    def test_soft_delete_vehicle(self):
        self.authenticate()
        response = self.client.post(reverse('vehicle-list-create'), self.vehicle_data, format='json')
        vehicle_id = response.data['data']['id']
        response = self.client.delete(reverse('vehicle-detail', args=[vehicle_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('vehicle-list-create'))
        self.assertEqual(len(response.data['data']), 0)

    def test_vehicle_year_invalid(self):
        self.authenticate()
        invalid_data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 202,  # Invalid: not 4 digits
            "plate": "AB-1234"
        }
        response = self.client.post(reverse('vehicle-list-create'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 0)
        self.assertIn("year", response.data['data'])
