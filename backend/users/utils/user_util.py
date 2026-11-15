# Parsear la informacion del usuario en un diccionario
def parse_data_user(username, email, password, avatar, is_register):
    return {
        'username': username,
        'first_name': username,
        'email': email,
        'password': password,
        'avatar': avatar,
        'is_register': is_register,
    }
