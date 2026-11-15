from django.db import transaction, DatabaseError
from users.utils.user_validator import (
        validate_username, validate_email, validate_password, validate_existence
    )
from users.utils.user_util import parse_data_user
from users.schemas.user_schema import RegisterPayload
from users.models import User

def register_user(payload: RegisterPayload):

    validation = validate_username(payload.username)
    if not validation["success"]:
        return validation

    validation = validate_email(payload.email)
    if not validation["success"]:
        return validation

    validation = validate_existence(payload.username, payload.email)
    if not validation["success"]:
        return validation

    validation = validate_password(payload.password, payload.repeat_password)
    if not validation["success"]:
        return validation

    data_user = parse_data_user(payload.username, payload.email, payload.password, None, False)

    try:
        with transaction.atomic():
            User.objects.create_user(**data_user)

        return {
                'success': True,
                'message_error': "",
            }
    except DatabaseError as error:
        return {
            'success': False,
            'message_error': "Ha habido un error al crear el usuario: " + str(error),
        }

    
