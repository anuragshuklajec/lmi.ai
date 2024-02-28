from django.db import models

class CustomUser(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    dob = models.DateField()
    email = models.EmailField()
    password = models.EmailField()

