from django.conf import settings
from twilio.rest import Client

account_sid = settings.TWILIO_SID
auth_token = settings.TWILIO_AUTH_TOKEN
twilio_sender = settings.TWILIO_SENDER_PHONE


def send_activation_sms(user):
    receiver = str(user.phone_number)
    code = user.activation_code
    message = f'Ваш код активации: {code}'
    client = Client(account_sid, auth_token)
    client.messages.create(body=message,
                           from_=twilio_sender,
                           to=receiver)

