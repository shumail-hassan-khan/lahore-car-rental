from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    plate = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.make} {self.model} - {self.plate}"
