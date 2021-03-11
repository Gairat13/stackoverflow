from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.utils import send_activation_sms

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirmation = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('phone_number', 'username', 'password', 'password_confirmation')

    def validate_phone_number(self, phone_number):
        if MyUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Пользователь с данным номером уже существует!')
        return phone_number

    def validate_username(self, username):
        if MyUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Пользователь с данным именем уже существует!')
        return username

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError('Пароли не совподают!')
        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        send_activation_sms(user)
        return user