import jwt
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from ninja_jwt.exceptions import InvalidToken, TokenError


from users.models import User
from users.validators.auth_validator import validate_free_user
from users.validators.general_validator import validate_username, validate_password
from users.validators.user_validator import validate_avatar
from users.schemas.user_schema import SetUserPayload

# Edita el nombre de usuario, nombre visible, la contraseña y la imagen
def set_user(payload: SetUserPayload):
    
    try:
        with transaction.atomic():
            is_validate = validate_username(payload.username)
            if not is_validate['success']:
                return {
                    'success': False,
                    'message_error': is_validate['message_error'],
                }

            is_validate = validate_free_user(payload.username, '')
            if not is_validate['success']:
                return {
                    'success': False,
                    'message_error': is_validate['message_error'],
                }
            
            payload.user.username = payload.username

            if payload.first_name.lower() != payload.username.lower():
                return {
                    'success': False,
                    'message_error': 'Tu nombre debe ser igual a tu username solo puedes modificar las mayusculas y minusculas'
                }

            payload.user.first_name = payload.first_name

            is_validate = validate_password(payload.password)
            if not is_validate['success']:
               return {
                  'success': False,
                  'message_error': is_validate['message_error'],
               }

            if payload.img_avatar != None:
                is_validate = validate_avatar(payload.img_avatar)
                if is_validate['success']:
                    return {
                        'success': False,
                        'message_error': is_validate['message_error'],
                    }

                payload.user.avatar = payload.img_avatar
            payload.user.save()
        return {
            'success': True,
            'message_error': "",
        }
    except DatabaseError:
        return {
            'success': False,
            'message_error': "Parece ser que hay un problema al conectar con la base de datos"
        }

# Obtiene informacion importante de tu propio usuario sin revelar demasiado
def get_me(request, token: str | None = None):
  jwt_auth = JWTAuth()
  auth_header = (
      f"Bearer {token}" if token else request.headers.get("Authorization")
  )

  if not auth_header or not auth_header.startswith("Bearer "):
    return {
        "success": False,
        "message_error": "Token no proporcionado o formato inválido.",
        "data": None,
    }

  try:
    user = jwt_auth.authenticate(request, auth_header)
    if not user:
      return {
          "success": False,
          "message_error": "Token inválido o usuario no encontrado.",
          "data": None,
      }

    return {
        "success": True,
        "message_error": "",
        "data": {
            "username": user.username,
            'first_name': user.first_name,
            'avatar': user.avatar,
            "email": user.email,
        },
    }

  except (InvalidToken, TokenError):
    return {
        "success": False,
        "message_error": "El token ha expirado o no es válido.",
        "data": None,
    }