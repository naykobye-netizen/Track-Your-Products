from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets

# Esta clase representa un usuario en el sistema
class User(AbstractUser):
    last_name = None
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

# Esta clase representa un codigo de verificacion para un usuario
class Verification(models.Model):
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()

    # Añade 15 minutos a la fecha en la que se crea para el tiempo de expiracion
    def add_fifteen_minutes():
        return timezone.now() + timedelta(minutes=15)
    
    at_expire = models.DateTimeField(default=add_fifteen_minutes)

    # Crea el token temporal de la validacion para cosas como recuperar la contraseña entre otras cosas
    def create_tmp_token():
        return secrets.token_urlsafe(64)

    tmp_token = models.CharField(max_length=255, default=create_tmp_token, editable=False)
    attempts = models.IntegerField(default=0)