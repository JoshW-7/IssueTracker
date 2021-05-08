from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import routers

from .views import DashboardView, ProjectView, IssueView, CreateIssueView, CreateProjectView


urlpatterns = [
    path('', DashboardView.as_view(), name="issues"),
    path('project/<int:project_id>/', login_required(ProjectView.as_view()), name="project"),
    path('issue/<int:issue_id>/', login_required(IssueView.as_view()), name="issue"),
    path('create_project/', login_required(CreateProjectView.as_view()), name="create_project"),
    path('create_issue/', login_required(CreateIssueView.as_view()), name="create_issue"),
]
