from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from users.controllers.user_controller import UsersController

api = NinjaExtraAPI()

api.register_controllers(
    NinjaJWTDefaultController,
    UsersController
)