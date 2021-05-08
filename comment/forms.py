from django.forms import ModelForm
from django import forms

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "style": "resize: vertical; min-height: 60px; max-height: 240px; min-width: 100%;",
                "rows": "4",
                "type": "text",
                "maxlength": "2000",
            }),
        }