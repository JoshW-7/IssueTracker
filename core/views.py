import os

from django.shortcuts import render
from rest_framework import viewsets
from django.views.static import serve

from issue.serializers import TagSerializer, IssueSerializer, StatusSerializer, ProjectSerializer
from issue.models import Tag, Issue, Status, Project


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer