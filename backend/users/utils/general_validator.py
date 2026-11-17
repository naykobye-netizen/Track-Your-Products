from PIL import Image, UnidentifiedImageError
import unicodedata

# Valida si el username del usuario cumple con las condiciones de longitud y caracteres permitidos
def validate_username(username: str):

    if (len(username) > 30 or len(username) < 5):
        return {
            'success': False,
            'message_error': "El nombre de usuario debe tener entre 5 a 30 caracteres.",
        }

    if (not username.isascii() or not username.isalpha() or not username.islower()):
        return {
            'success': False,
            'message_error': "El nombre de usuario solo puede tener letras y solo en minusculas.",
        }

    return {
        'success': True,
        'message_error': "",
    }

# Valida si el email del usuario cumple con las condiciones de formato y caracteres permitidos
def validate_email(email: str):

    user_email = email[:email.find('@')]
    domain = email[email.find('@')+1:]

    if (    
            email.count("@") != 1
            or domain.count('.') < 1
            or user_email == ""  
            or domain[:domain.find('.')] == ""
            or email.rfind('.') == len(email) - 1
            or len(email[email.rfind('.')+1:]) < 2
            or ".." in domain
            or "." ==  domain[0]
            or "-" ==  domain[0]
            or "-." in domain
            or ".-" in domain
            or any(char.isspace() for char in email)
            or domain.endswith("-")
            or not all(
                char.isascii() and (char.isalnum() or char in ".-")
                for char in domain
            )
            or not email[email.rfind('.') + 1:].isalpha()
        ):
            return {
                'success': False,
                'message_error': "El formato del correo no es correcto"
            }

    return {
        'success': True,
        'message_error': "",
    }


# Valida si la contraseña del usuario cumple con las condiciones de longitud, caracteres permitidos y coincidencia con la contraseña repetida
def validate_password(password: str, repeat_password: str):
    if (len(password) > 30 or len(password) < 5):
            return {
                'success': False,
                'message_error': "La contraseña debe tener entre 5 a 30 caracteres.",
            }
    
    if (
            not any(char.isdigit() for char in password) 
            or not any(
                unicodedata.category(char)[0] in ("S", "P")
                for char in password
            )
        ):
        return {
            'success': False,
            'message_error': "La contraseña debe tener al menos un numero y al menos un caracter especial",
        }

    if (password != repeat_password):
        return {
            'success': False,
            'message_error': "Las contraseñas no coinciden",
        }

    return {
        'success': True,
        'message_error': "",
    }


# Valida si el avatar del usuario cumple con las condiciones de tamaño, formato y dimensiones
def validate_avatar(img_avatar):

    if img_avatar.size > 2097152:
        return {
            'success': False,
            'message_error': "La imagen no puede superar los 2 MB.",
        }

    try:
        img = Image.open(img_avatar)

        if img.format not in ("JPEG", "PNG", "WEBP"):
            img_avatar.seek(0)
            return {
                'success': False,
                'message_error': "El formato de imagen no está permitido.",
            }

        if (img.width > 4096 or img.height > 4096):
            img_avatar.seek(0)
            return {
                'success': False,
                'message_error': "La imagen debe medir de alto maximo 4096px y de ancho maximo 4096px",
            }

        img.verify()

        img_avatar.seek(0)

    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        return {
            'success': False,
            'message_error': "El archivo no es una imagen válida.",
        }

    return {
        'success': True,
        'message_error': "",
    }