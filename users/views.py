from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from utils.response_format import success_response, error_response 
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return success_response("User registered successfully", data, status_code=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            message = ""
            for field, msgs in errors.items():
                message += f"{field}: {', '.join(msgs)}; "
            message = message.strip()
            return error_response("Registration failed: " + message)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return success_response("Login successful", serializer.validated_data)
        except Exception as e:
            detail = getattr(e, 'detail', "Invalid credentials")
            return error_response("Login failed", detail, status_code=status.HTTP_401_UNAUTHORIZED)

