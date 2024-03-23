from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class CustomUser(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    is_hr = models.BooleanField(default=False)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    password = models.EmailField()

    def clean(self):
        super().clean()
        if not self.email:
            raise ValidationError("Email field is required")
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError("Invalid email address")

class Organisation(models.Model):
    name = models.CharField(max_length = 25,unique = True)
    hr = models.ForeignKey(CustomUser,on_delete = models.CASCADE)

class Interview(models.Model):
    title = models.CharField(max_length = 50)
    role = models.CharField(max_length = 50)
    jd = models.TextField()
    yoe = models.IntegerField(default = 0)
    organisation = models.ForeignKey(Organisation, models.CASCADE)

class InterviewDetail(models.Model):
    email = models.EmailField(null=True)
    candidate = models.ForeignKey(CustomUser,on_delete = models.CASCADE,null=True)
    interview = models.ForeignKey(Interview,on_delete = models.CASCADE)
    is_accepted = models.BooleanField(default = False)
    is_declined = models.BooleanField(default = False)
    is_attempted = models.BooleanField(default = False)
    questions = models.JSONField(null = True)
    answers = models.JSONField(null = True)
    expiry = models.DateTimeField(null = True)


