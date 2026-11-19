from ninja import Schema
from PIL import Image

from users.models import User

# Define el esquema de datos para la modificacion de datos del usuario, incluyendo el usuario, nombre de usuario, nombre visible, contraseña y imagen en caso que quieras.
class SetUserPayload(Schema):
    user: User
    username: str
    first_name: str
    password: str
    img_avatar: Image | None
