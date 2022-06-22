from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(reciever, token):
        email = EmailMessage(
            subject='Yamdb',
            body=f'Access Token: {token}',
            to=[reciever]
        )
        email.send()

