from rest_framework import serializers
from .models import Vehicle
from django.contrib.auth.models import User
import re

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class VehicleSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'plate', 'user']

    def validate_make(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("Make must contain only letters (A-Z or a-z).")
        return value

    def validate_model(self, value):
        if not re.match(r'^[a-zA-Z]+$', value):
            raise serializers.ValidationError("Model must contain only letters (A-Z or a-z), no numbers or special characters.")
        return value

    def validate_year(self, value):
        if not re.match(r'^\d{4}$', str(value)):
            raise serializers.ValidationError("Year must be exactly 4 digits.")
        return value

    def validate_plate(self, value):
        if not re.match(r'^([A-Z]{3}-\d{3}|[A-Z]{2}-\d{4})$', value.upper()):
            raise serializers.ValidationError("Plate must be in format 'ABC-123' or 'AB-1234'.")
        return value