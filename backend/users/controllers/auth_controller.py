from ninja_extra import api_controller, ControllerBase, route

from users.services.auth_service import (
    register_user, verify_user, 
    login_user, request_password_recovery, 
    verify_password_recovery, reset_password
)
from users.schemas.auth_schema import (
    GenericOut, VerifyOut, 
    RegisterPayload, LoginPayload, 
    ResetPasswordPayload, VerifyPayload
)

# Controlador para manejar las operaciones relacionadas con la autenticacion de usuarios
@api_controller('/auth', tags=['Users'])
class AuthController(ControllerBase):

    # Endpoint para registrar un nuevo usuario en el sistema
    @route.post('/register', response=GenericOut)
    def register(self, payload: RegisterPayload):
        return register_user(payload)

    # Endpoint para iniciar sesión un usuario en el sistema
    @route.post('/login', response=GenericOut)
    def login(self, payload: LoginPayload):
        return login_user(payload)

    # Endpoint para solicitar un codigo de recuperacion de contraseña a partir del email del usuario
    @route.get('/recover-password/request', response=GenericOut)
    def request_verification(self, username: str):
        return request_password_recovery(username)

    # Endpoint para verificar un codigo de recuperacion de contraseña y obtener el id del usuario
    @route.post('/recover-password/verify')
    def verify_recovery(self, payload: VerifyPayload):
        return verify_password_recovery(payload)

    # Endpoint para resetear la contraseña de un usuario a partir de su id y la nueva contraseña
    @route.post('/recover-password/reset', response=GenericOut)
    def reset(self, payload: ResetPasswordPayload):
        return reset_password(payload)

    # Endpoint para verificar un usuario a partir de un codigo de verificacion
    @route.post('/verify', response=VerifyOut)
    def verify(self, payload: VerifyPayload):
        return verify_user(payload)