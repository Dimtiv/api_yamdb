from django.core.mail import EmailMessage


class Email:
    DEFAULT_SUBJECT = 'Yamdb'

    @staticmethod
    def send_email(reciever, body, subject=DEFAULT_SUBJECT):
        email = EmailMessage(
            subject=subject,
            body=body,
            to=[reciever]
        )
        email.send()
