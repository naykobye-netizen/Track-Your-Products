from ninja import Schema

class RegisterPayload(Schema):
    username: str
    email: str
    password: str
    repeat_password: str

class RegisterOut(Schema):
    success: bool
    message_error: str
