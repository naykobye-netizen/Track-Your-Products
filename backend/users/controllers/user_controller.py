from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth

from users.services.user_service import register_user
from users.schemas.user_schema import RegisterOut, RegisterPayload


@api_controller('/users', tags=['Users'])
class UsersController(ControllerBase):

    # Registrar un usuario
    @route.post('/register', response=RegisterOut)
    def register(self, payload: RegisterPayload):
        return register_user(payload)