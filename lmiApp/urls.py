
from django.urls import path
from .views import *


urlpatterns = [
    path('createOrganisation',createOrganisation),
    path('createInterview',createInterview),
    path('sendInvites',sendInvites),
    path('acceptInvite',acceptInvite),
    path('declineInvite',declineInvite),
    path('sendReminder',sendReminder),
]

