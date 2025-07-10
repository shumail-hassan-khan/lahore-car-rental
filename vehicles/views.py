from rest_framework import generics, permissions
from .models import Vehicle
from .serializers import VehicleSerializer
from utils.response_format import success_response, error_response


class VehicleListCreateView(generics.ListCreateAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user, is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response("Vehicle list fetched successfully", serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response("Vehicle created successfully", serializer.data, status_code=201)
        return error_response("Validation failed", serializer.errors)


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user, is_deleted=False)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response("Vehicle fetched successfully", serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Vehicle updated successfully", serializer.data)
        return error_response("Validation failed", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return success_response("Vehicle deleted successfully", {})
