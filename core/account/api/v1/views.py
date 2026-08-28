from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core import settings
from .serializer import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
)
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from account.models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

User = get_user_model()


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email": email,
            }
            user_obj = get_object_or_404(User, email=email)
            token = get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/email_template.tpl",
                {"token": token},
                from_email="from@email.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        elif hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer
    model = User

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if not user.check_password(serializer.data["old_password"]):
                return Response(
                    {"old_password": ["wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": ["password has been changed"]},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.queryset
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class SendEmailView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        email = "m.ina.m.van@gmail.com"
        user_obj = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/email_template.tpl",
            {"token": token},
            from_email="from@email.com",
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response({"detail": "email has been sent"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)


class AccountActivationView(APIView):

    def post(self, request, token, *args, **kwargs):
        try:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]).get(
                "user_id"
            )
            user_obj = get_object_or_404(User, pk=user_id)
            if user_obj.is_verified:
                return Response(
                    {"detail": "user already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_obj.is_verified = True
            user_obj.save()
            return Response(
                {"detail": "user has been activated"},
                status=status.HTTP_200_OK,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "token is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.InvalidTokenError:
            return Response(
                {"detail": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "user does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccountResendActivationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        email = request.user.email
        if email:
            user_obj = get_object_or_404(User, email=email)
            token = get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/email_template.tpl",
                {"token": token},
                from_email="from@email.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(
                {"detail": "email has been sent"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "request failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
