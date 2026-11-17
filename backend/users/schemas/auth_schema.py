from ninja import Schema

# Define el esquema de datos para el registro de un usuario, incluyendo los campos necesarios para la solicitud y la respuesta.
class RegisterPayload(Schema):
    username: str
    email: str
    password: str
    repeat_password: str

# Define el esquema de datos para la respuesta del registro de un usuario, incluyendo el estado de éxito y un mensaje de error si corresponde.
class GenericOut(Schema):
    success: bool
    message_error: str

# Define el esquema de datos para la solicitud de verificación de un usuario, incluyendo el nombre de usuario y el código de verificación.
class LoginPayload(Schema):
    username: str
    password: str

# Define el esquema de datos para la solicitud de verificación de un usuario, incluyendo el nombre de usuario y el código de verificación.
class ResetPasswordPayload(Schema):
    tmp_token: str
    username: str
    password: str
    repeat_password: str

# Define el esquema de datos para la solicitud de verificación de un usuario, incluyendo el nombre de usuario y el código de verificación.
class VerifyPayload(Schema):
    username: str
    code: str

# Define el esquema de datos para la respuesta de la verificación de un usuario, incluyendo el estado de éxito, un mensaje de error y un token si corresponde.
class VerifyOut(Schema):
    success: bool
    message_error: str
    token: str