from django import forms
from django.forms import ModelForm

from .models import Issue, Tag, Project


tag_count = Tag.objects.all().count()
tag_widget_height = tag_count * 18


class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "project", "status", "tags", "user"]
        widgets = {
            "title": forms.TextInput(attrs={
                "style": "height: 20px; flex-grow: 1;",
                "maxlength": "200",
            }),
            "description": forms.Textarea(attrs={
                "style": "flex-grow: 1;resize: vertical; min-height: 60px; max-height: 240px;",
                "rows": "4",
                "type": "text",
                "maxlength": "2000",
            }),
            "project": forms.Select(attrs={
                "style": "flex-grow: 1; height: 25px;",
            }),
            "status": forms.Select(attrs={
                "style": "flex-grow: 1; height: 25px;",
            }),
            "tags": forms.SelectMultiple(attrs={
                "style": f"flex-grow: 1; height: {tag_widget_height}px",
            }),
            "user": forms.Select(attrs={
                "style": "height: 25px;",
            })
        }

    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "style": "height: 20px; flex-grow: 1;",
                "maxlength": "200",
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)


class UploadFileForm(forms.Form):
    file = forms.FileField()


       