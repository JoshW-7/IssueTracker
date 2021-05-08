from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import User

from issue.models import Issue


class Comment(TimeStampedModel):
    # user = models.ForeignKey("User", null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=100)
    text = models.TextField(default="")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
