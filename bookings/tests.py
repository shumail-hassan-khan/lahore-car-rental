from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from bookings.models import Booking
from datetime import date, timedelta

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.vehicle = Vehicle.objects.create(
            make="Honda", model="Civic", year=2020, plate="ABC-123", user=self.user
        )
        self.booking_url = reverse("booking-list")  

    def test_create_booking_success(self):
        data = {
            "vehicle_id": self.vehicle.id,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=2))
        }
        response = self.client.post(self.booking_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], 1)
        self.assertIn("Booking created successfully", response.data["message"])

    def test_create_booking_overlap_fails(self):
        Booking.objects.create(
            vehicle=self.vehicle,
            user=self.user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2)
        )
        data = {
            "vehicle_id": self.vehicle.id,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=1))
        }
        response = self.client.post(self.booking_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already booked", str(response.data["data"]).lower())


    def test_booking_invalid_date_range(self):
        data = {
            "vehicle_id": self.vehicle.id,
            "start_date": str(date.today() + timedelta(days=3)),
            "end_date": str(date.today())
        }
        response = self.client.post(self.booking_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("start date", str(response.data["data"]).lower())


    def test_booking_deleted_vehicle_fails(self):
        self.vehicle.is_deleted = True
        self.vehicle.save()
        data = {
            "vehicle_id": self.vehicle.id,
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=1))
        }
        response = self.client.post(self.booking_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("no longer available", str(response.data["data"]).lower())


    def test_booking_list_only_user_data(self):
        other_user = User.objects.create_user(username='other', password='otherpass')
        other_vehicle = Vehicle.objects.create(
            make="KIA", model="Sportage", year=2024, plate="XYZ-999", user=other_user
        )
        Booking.objects.create(
            vehicle=other_vehicle,
            user=other_user,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1)
        )
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(booking['vehicle']['user']['id'] == self.user.id for booking in response.data['data']))
