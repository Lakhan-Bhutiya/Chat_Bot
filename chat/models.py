from django.db import models
from django.utils import timezone

class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_and_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question
