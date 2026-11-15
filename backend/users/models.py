from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    last_name = None
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_register = models.BooleanField(default=False)

class Verification(models.Model):
    owner_user = models.ForeignKey(to=User, on_delete=models.CASCADE, unique=True)
    code = models.IntegerField()

    # Esta funcion añade 15 minutos a la fecha en la que se crea para el tiempo de expiracion
    def add_fifteen_minutes():
        return timezone.now() + timedelta(minutes=15)
    
    at_expire = models.DateTimeField(default=add_fifteen_minutes())