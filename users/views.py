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
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.data['username'],
            password=serializer.data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login Successful'
            }, status=status.HTTP_200_OK)
        return Response({'error: Login Failed'}, status=status.HTTP_400_BAD_REQUEST)

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
            fail_silently=False,
        )