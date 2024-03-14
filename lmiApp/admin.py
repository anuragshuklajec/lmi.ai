from django.contrib import admin
from .models import CustomUser,Organisation,Interview,InterviewDetail
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Organisation)
admin.site.register(Interview)
admin.site.register(InterviewDetail)