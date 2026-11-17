from ninja_extra import NinjaExtraAPI

from users.controllers.auth_controller import AuthController

user_api = NinjaExtraAPI()

user_api.register_controllers(
    AuthController,
)