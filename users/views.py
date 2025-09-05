from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from tasmapoisk import settings
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, FeedbackSerializers
from .models import Feedback

@extend_schema(summary='Регистрация', tags=['Movie'])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

@extend_schema(summary='Логин', tags=['Movie'])
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        # если JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


@extend_schema(summary='Профиль', tags=['Movie'])
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

@extend_schema(summary='Обратная связь', tags=['Movie'])
class FeedbackSendView(generics.CreateAPIView):
    serializer_class = FeedbackSerializers
    queryset = Feedback.objects.all()

    def perform_create(self, serializer):
        feedback = serializer.save()
        subject = f'Обратная связь от {feedback.name}'
        full_message = f'Имя: {feedback.name}\nEmail: {feedback.email}\nMessage: {feedback.message}'

        send_mail(
            subject,
            full_message,
            feedback.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False
        )