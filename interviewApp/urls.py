from django.urls import path
from .views import *

urlpatterns = [
    path('starttest',startTest),
    path('givetest',giveTest),
    path('evaluateTest',evaluateCandidate),
]