from rest_framework import serializers
from .models import Booking
from vehicles.serializers import VehicleSerializer
import datetime
from .models import Vehicle


class BookingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.filter(is_deleted=False),
        write_only=True,
        source='vehicle'
    )

    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'vehicle_id', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        vehicle = data.get('vehicle')

        if start_date > end_date:
            raise serializers.ValidationError("Start date must be before or equal to end date.")

        if vehicle and vehicle.is_deleted:
            raise serializers.ValidationError("This vehicle is no longer available for booking.")

        return data


