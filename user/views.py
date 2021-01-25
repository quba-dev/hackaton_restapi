from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationAPISerializer, LoginSerializer
from .utils import send_activation_mail
from rest_framework_simplejwt.views import TokenObtainPairView



User = get_user_model()


class RegistrationAPIView(APIView):

    def post(self, request):

        serializer = RegistrationAPISerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                user.create_activation_code()
                send_activation_mail(user.email, user.activation_code)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

class ActivationView(APIView):

    def get(self, request, activation_code):

        user = get_object_or_404(User, activation_code=activation_code)
        user.activate_with_code(activation_code)
        return Response(data={'message': 'Аккаунт успешно активирован'}, status=200)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы удачно разлогинились.', status=status.HTTP_200_OK)

