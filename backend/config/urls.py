from django.contrib import admin
from django.urls import path
from users.api import user_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", user_api.urls),
]
