from flask import render_template

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
    msg.html = render_template("confirm_account_email.html", confirm_url=link)
    try:
        mail.send(msg)
    except Exception as e:
        print(e)
        raise MailException("Unable to send email")
