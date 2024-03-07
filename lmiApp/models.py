from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomUser(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    dob = models.DateField()
    email = models.EmailField()
    password = models.EmailField()

    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError("Email field is required")
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError("Invalid email address")
