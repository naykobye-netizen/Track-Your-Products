from users.models import User
from django.utils import timezone

# Valida si el username y el email del usuario ya existen en la base de datos
def validate_free_user(username: str, email: str):
    try:
        user = User.objects.get(username=username)
        return {
            'success': False,
            'message_error': "Este username no esta disponible.",
            'user': user
        }
    except User.DoesNotExist:
        pass

    if email != '':
        try:
            user = User.objects.get(email=email)
            return {
                'success': False,
                'message_error': "Este correo no esta disponible.",
                'user': user
            }
        except User.DoesNotExist:
            pass

    return {
        'success': True,
        'message_error': "",
    }

# Verifica si el codigo de verificacion ha expirado
def is_expired_verify(verification: str):
    
    expiration = verification.at_expire

    now = timezone.now()

    if now >= expiration:
        verification.delete()
        return {
            'success': False,
            'message_error': "El codigo ha expirado.",
        }

    if verification.attemps >= 5:
        verification.delete()
        return {
            'success': False,
            'message_error': "A superado el numero maximo de intentos permitidos para este codigo.",
        }

    return {
        'success': True,
        'message_error': "",
    }

# Verifica si el codigo de verificacion es correcto
def is_correct_code_verify(verification: str, code: str):
    if verification.code != int(code):
        verification.attemps += 1
        verification.save()
        return {
            'success': False,
            'message_error': "El codigo es incorrecto.",
        }

    return {
        'success': True,
        'message_error': "",
    }

# Verifica si el token temporal de verificacion es correcto
def is_correct_tmp_token_verify(verification: str, tmp_token: str):
    if verification.tmp_token != tmp_token:
        return {
            'success': False,
            'message_error': "El token temporal es incorrecto.",
        }

    return {
        'success': True,
        'message_error': "",
    }