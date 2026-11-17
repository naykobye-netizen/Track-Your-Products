from django.db import transaction, DatabaseError
from ninja_jwt.tokens import AccessToken

from users.utils.auth_validator import (
    validate_free_user, is_expired_verify, 
    is_correct_code_verify, is_correct_tmp_token_verify
)
from users.utils.auth_util import (
    parse_data_user, create_code_verify, 
    create_expire_data_code_verify, 
    load_email_html_verify, send_email_verify, 
    get_verification
)
from users.utils.general_validator import (
    validate_username, validate_email, 
    validate_password
)
from users.schemas.auth_schema import (
    RegisterPayload, LoginPayload, 
    ResetPasswordPayload, VerifyPayload
)
from users.models import User, Verification

# Registrar un nuevo usuario en el sistema y envia un codigo de verificacion al email del usuario
def register_user(payload: RegisterPayload):

    validation = validate_username(payload.username)
    if not validation["success"]:
        return validation

    validation = validate_email(payload.email)
    if not validation["success"]:
        return validation

    validation = validate_password(payload.password, payload.repeat_password)
    if not validation["success"]:
        return validation
    try:
        with transaction.atomic():
            validation = validate_free_user(payload.username, payload.email)
            if not validation["success"]:
                user = validation['user']
                if (not user.is_verified):
                    user.delete()
                else:
                    return validation

            data_user = parse_data_user(payload.username, payload.email, payload.password, None, False)
            user = User.objects.create_user(**data_user)
            code = create_code_verify()
            expire_date = create_expire_data_code_verify()
            Verification.objects.create(owner_user=user, code=code, at_expire=expire_date)
            html_email = load_email_html_verify(code)
            send_email_verify(code, html_email, payload.email)

        return {
                'success': True,
                'message_error': "",
            }
    except DatabaseError:
        return {
            'success': False,
            'message_error': "Ha habido un error al crear el usuario",
        }

# Inicia sesión un usuario en el sistema y devuelve un token de acceso si las credenciales son correctas
def login_user(payload: LoginPayload):

    validation = validate_username(payload.username)
    if not validation["success"]:
        return validation

    validation_free_user = validate_free_user(payload.username, '')
    if validation_free_user["success"]:
        return {
            'success': False,
            'message_error': "La contraseña o el usuario es incorrecto.",
        }

    validation = validate_password(payload.password, payload.password)
    if not validation["success"]:
        return validation
    
    try:
        with transaction.atomic():
            user = validation_free_user['user']
            if not user.check_password(payload.password):
                return {
                    'success': False,
                    'message_error': "La contraseña o el usuario es incorrecto.",
                }
            if not user.is_verified:
                return {
                    'success': False,
                    'message_error': "El usuario no ha sido verificado.",
                }
            
            code = create_code_verify()
            expire_date = create_expire_data_code_verify()

            if Verification.objects.filter(owner_user=user).exists():
                verification = Verification.objects.get(owner_user=user)
                verification.code = code
                verification.at_expire = expire_date
                verification.save()
            else:
                Verification.objects.create(owner_user=user, code=code, at_expire=expire_date)

            html_email = load_email_html_verify(code)
            send_email_verify(code, html_email, user.email)

        return {
            'success': True,
            'message_error': "",
        }
    except DatabaseError:
        return {
            'success': False,
            'message_error': "Ha habido un error al iniciar sesión",
        }

# Verifica un usuario a partir de un codigo de verificacion
def verify_user(payload: VerifyPayload):

    response_verification = get_verification(payload.username)
    if not response_verification['success']:
        return {
            'success': response_verification['success'],
            'message_error': response_verification['message_error'],
            'token': ""
        }

    verification = response_verification['verification']

    is_expired = is_expired_verify(verification)
    if (is_expired['success'] == False):
        return {
            'success': is_expired['success'],
            'message_error': is_expired['message_error'],
            'token': ""
        }
    
    response_verification = is_correct_code_verify(verification, payload.code)
    if (response_verification['success'] == False):
        return {
            'success': response_verification['success'],
            'message_error': response_verification['message_error'],
            'token': ""
        }

    user = verification.owner_user
    if not user.is_verified:
        user.is_verified = True
        user.save()

    verification.delete()

    return {
        'success': True,
        'message_error': "",
        'token': str(AccessToken.for_user(user)),
    }

# Solicita la recuperacion de contraseña de un usuario a partir de su email y envia un codigo de recuperacion al email del usuario
def request_password_recovery(username: str):
    validation = validate_username(username)
    if not validation["success"]:
        return validation

    validation = validate_free_user(username, '')
    user = validation['user']
    if validation["success"]:
        return {
            'success': False,
            'message_error': "El usuario no es incorrecto.",
        }

    if (user.is_verified == False):
        return {
            'success': False,
            'message_error': "El usuario no ha sido verificado.",
        }

    code = create_code_verify()
    expire_date = create_expire_data_code_verify()

    verification = get_verification(username)

    if verification['success'] and verification['verification']:
        verification = verification['verification']
        verification.code = code
        verification.at_expire = expire_date
        verification.save()
    else:
        Verification.objects.create(owner_user=user, code=code, at_expire=expire_date)

    html_email = load_email_html_verify(code)
    send_email_verify(code, html_email, user.email)

    return {
        'success': True,
        'message_error': "",
    }

# Verifica el codigo de recuperacion de contraseña y devuelve el id del usuario si es valido
def verify_password_recovery(payload: VerifyPayload):
    response_verification = get_verification(payload.username)
    if (response_verification['success'] == False):
        return response_verification

    verification = response_verification['verification']

    is_expired = is_expired_verify(verification)
    if (is_expired['success'] == False):
        return is_expired
    
    response_verification = is_correct_code_verify(verification, payload.code)
    if (response_verification['success'] == False):
        return {
            'success': False,
            'message_error': response_verification['message_error']
        }

    return {
        'success': True,
        'message_error': "",
        'tmp_token': verification.tmp_token,
    }

# Resetea la contraseña de un usuario a partir de su id y la nueva contraseña
def reset_password(payload: ResetPasswordPayload):
    verification__response = get_verification(payload.username)
    if (verification__response['success'] == False):
        return verification__response
    
    validation = is_correct_tmp_token_verify(verification__response['verification'], payload.tmp_token)
    if (validation['success'] == False):
        return validation
    
    validation = validate_password(payload.password, payload.repeat_password)
    if not validation["success"]:
        return validation

    response_free_user = validate_free_user(payload.username, '')
    if response_free_user["success"]:
        return {
            'success': False,
            'message_error': "El usuario no es incorrecto.",
        }
    user = response_free_user['user']
    user.set_password(payload.password)
    user.save()

    return {
        'success': True,
        'message_error': "",
    }