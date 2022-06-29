from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(reciever, confirmation_code):
        email = EmailMessage(
            subject='Yamdb',
            body=f'Ваш код подтверждения: {confirmation_code}',
            to=[reciever]
        )
        email.send()

