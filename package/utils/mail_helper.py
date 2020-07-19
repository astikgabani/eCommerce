from flask_mail import Message

from plugins.mail import mail


class MailException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def send_confirmation_mail(email, link):
    if not email:
        raise MailException("Email is not provided")

    msg = Message(subject="Registration Verification")
    msg.add_recipient(email)
    msg.body = f"Please click the link to confirm your registration: {link}"
    try:
        mail.send(msg)
    except Exception as e:
        print(e)
        raise MailException("Unable to send email")
