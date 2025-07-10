from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.vehicle} from {self.start_date} to {self.end_date}"

    def vehicle_owner(self):
        return self.vehicle.user
