from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth


# Controlador para manejar las operaciones relacionadas con los usuarios
@api_controller('', tags=['Users'])
class UsersController(ControllerBase):