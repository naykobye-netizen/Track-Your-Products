from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from users.models import Verification, User
from users.validators.auth_validator import validate_free_user

# Parsea los datos del usuario para crear un nuevo usuario
def parse_data_user(username: str, email: str, password: str, avatar, is_verified: bool):
    if username == None or email == None or password == None or is_verified == None:
        return {
            'success': False,
            'message_error': "Falta informacion del usuario"
        }
    
    return {
        'success': True,
        'username': username,
        'first_name': username,
        'email': email,
        'password': password,
        'avatar': avatar,
        'is_verified': is_verified,
        'date_joined': timezone.now(),
    }

# Genera un codigo de verificacion aleatorio de 6 digitos
def create_code_verify():
    return get_random_string(
        length=6,
        allowed_chars="0123456789"
    )

# Genera la fecha de expiracion del codigo de verificacion
def create_expire_data_code_verify():
    return timezone.now() + timedelta(minutes=10)

# Obtiene la verificacion a partir del codigo de verificacion
def get_verification(email_or_username: str):
    try:
        response_free_user = validate_free_user(username=email_or_username, email=email_or_username)
        if response_free_user['success']:
            return {
                'success': False,
                'message_error': "El usuario o correo es incorrecto",
                'verification': None
            }
        
        user = response_free_user['user']
        
        return {
            'success': True,
            'message_error': "",
            'verification': Verification.objects.get(owner_user=user)
        }


    except Verification.DoesNotExist:
        return {
            'success': False,
            'message_error': "El código de verificación no es válido",
            'verification': None
        }

# Carga el html del email de verificacion
def load_email_html_verify(code: str):
    return render_to_string(
        "verification_code.html",
        {
            "code": code
        }
    )

# Envía el email de verificación
def send_email_verify(code: str, html_email: str, to_send: str):
    email = EmailMultiAlternatives(
        subject="Verifica tu cuenta",
        body=f"Tu código de verificación es {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_send]
    )

    email.attach_alternative(
        html_email,
        "text/html"
    )

    email.send()