from PIL import Image, UnidentifiedImageError

# Valida si el avatar del usuario cumple con las condiciones de tamaño, formato y dimensiones
def validate_avatar(img_avatar: Image):

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

        if img.width > 4096 or img.height > 4096:
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

