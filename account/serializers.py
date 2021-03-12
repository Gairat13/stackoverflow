from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
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


class CreateNewPasswordSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    activation_code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_phone_number(self, phone):
        if not MyUser.objects.filter(phone_number=phone).exists():
            raise serializers.ValidationError('Пользователь с таким телефоном не найден')
        return phone

    def validate_activation_code(self, code):
        if not MyUser.objects.filter(activation_code=code, is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data()
        phone_number = data.get('phone_number')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(phone_number=phone_number,
                                      activation_code=activation_code,
                                      is_activa=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user



