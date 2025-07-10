from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView
from users.views import LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
