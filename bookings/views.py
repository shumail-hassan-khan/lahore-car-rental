from rest_framework import generics, permissions, status
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from utils.response_format import success_response, error_response


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.filter(user=user)

        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                queryset = queryset.filter(end_date__gte=from_date)
            except ValueError:
                pass 

        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                queryset = queryset.filter(start_date__lte=to_date)
            except ValueError:
                pass

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Bookings fetched successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = self.request.user
                vehicle = serializer.validated_data['vehicle']
                start_date = serializer.validated_data['start_date']
                end_date = serializer.validated_data['end_date']

                if start_date >= end_date:
                    raise ValidationError({"start_date": ["Start date must be before end date."]})

                if vehicle.is_deleted:
                    raise ValidationError({"vehicle": ["This vehicle is no longer available."]})

                overlap_exists = Booking.objects.filter(
                    vehicle=vehicle,
                    start_date__lte=end_date,
                    end_date__gte=start_date
                ).exists()

                if overlap_exists:
                    raise ValidationError({"vehicle": ["This vehicle is already booked during the selected dates."]})

                serializer.save(user=user)
                return success_response("Booking created successfully", serializer.data, status_code=status.HTTP_201_CREATED)

        except ValidationError as e:
            return error_response("Booking creation failed", e.detail)
