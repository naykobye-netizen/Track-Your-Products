from django.utils import timezone
from users.models import Verification

def is_expired_verify(user):
    try:
        object_verification = Verification.objects.get(owner_user=user)
    except Verification.DoesNotExist:
        return {
            'success': False,
            'message_error': "No existe verificacion para este usuario."
        }
    
    expiration = object_verification.at_expire

    now = timezone.now()

    if now >= expiration:
        object_verification.delete()
        return {
            'success': False,
            'message_error': "El codigo ha expirado.",
        }
    
    return {
        'success': True,
        'message_error': "",
    }
