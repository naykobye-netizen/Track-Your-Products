from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def create_code_verify():
    return get_random_string(
        length=6,
        allowed_chars="0123456789"
    )

def create_expire_data_code_verify():
    return timezone().now() + timedelta(minutes=10)

def load_email_html_verify(code):
    return render_to_string(
        "emails/verification_code.html",
        {
            "code": code
        }
    )

def send_email_verify(code, html_email, to_send):
    email = EmailMultiAlternatives(
        subject="Verifica tu cuenta",
        body=f"Tu código de verificación es {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_send
    )

    email.attach_alternative(
        html_email,
        "text/html"
    )

    email.send()
