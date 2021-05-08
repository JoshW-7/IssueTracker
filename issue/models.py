import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Statuses"


class Project(TimeStampedModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Issue(TimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    status = models.ForeignKey("Status", null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey("Project", blank=True, null=True, on_delete=models.SET_NULL)

    relations = models.ManyToManyField("Issue", blank=True, related_name="parent")
    tags = models.ManyToManyField("Tag", blank=True, related_name="issue")
    files = models.ManyToManyField("File", blank=True, related_name="issue")

    def __str__(self):
        return self.title

    def tag_list(self) -> str:
        return ", ".join([tag.name for tag in self.tags.all()])


class File(models.Model):
    file = models.FileField(upload_to="files/")

    def __str__(self):
        return self.file.name

    @property
    def relative_path(self):
        return os.path.relpath(self.file.path, settings.MEDIA_ROOT)

    @property
    def filename(self):
        return self.file.name.split("files/")[-1]