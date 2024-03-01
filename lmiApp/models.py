from django.db import models


# Create your models here.
class QuestionRequest(models.Model):
    technology = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    number_of_questions = models.IntegerField()


class EvaluateRequest(models.Model):
    # Assuming questions and answers are stored as JSON strings
    questions = models.JSONField()
    answers = models.JSONField()


class QuestionResponse(models.Model):
    generated_questions = models.JSONField()


class EvaluationResponse(models.Model):
    evaluation_result = models.CharField(max_length=100)
