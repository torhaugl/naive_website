import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_txt = models.CharField("Question text", max_length=200)
    pub_data = models.DateTimeField("Date published")

    def __str__(self):
        return self.question_txt

    def was_published_recently(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField("Choice text", max_length=200)
    votes = models.IntegerField("Votes", default=0)

    def __str__(self):
        return self.choice_text
