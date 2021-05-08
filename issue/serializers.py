from rest_framework import serializers

from .models import Project, Issue, Tag, Status


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ("id", "user", "created", "modified", "title", "description", "status", "relations", "tags", "project")

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "created", "modified", "name")

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name",)

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)