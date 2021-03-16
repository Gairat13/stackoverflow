from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, CreateNewPasswordSerializer
from account.tasks import send_activation_sms

MyUser = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('activation_code')
        user = MyUser.objects.filter(phone_number=phone, activation_code=code).first()
        if user is None:
            return Response('No such user', status=status.HTTP_400_BAD_REQUEST)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Successfully activated', status=status.HTTP_200_OK)


# api/v1/accounts/forgot_password/?phone=+996


class ForgotPassword(APIView):
    def get(self, request):
        phone = request.query_params.get('phone')
        print(phone)
        user = get_object_or_404(MyUser, phone_number=f'+{phone}')
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_sms.delay(str(user.phone_number), user.activation_code)
        return Response('Вам отправлено смс', status=status.HTTP_200_OK)


class ForgotPasswordComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=status.HTTP_200_OK)
