from django.core.mail import EmailMessage


def sendMail(title, message, to):
    email_message = EmailMessage(title, message, to=[to])
    email_message.send()
