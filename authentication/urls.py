
from django.urls import path
from .views import *

urlpatterns = [
    path("register/",register),
    path("login/",auth_login),
    path("logout/",auth_logout),
]

