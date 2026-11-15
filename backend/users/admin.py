from django.contrib import admin
from users.models import User, Verification

admin.site.register(User)
admin.site.register(Verification)