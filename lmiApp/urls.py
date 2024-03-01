
from django.urls import path
from .views import *


urlpatterns = [
    path("home/",home),
    path("get_questions", get_questions)
]


