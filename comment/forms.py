from .models import Comment
from django import forms 
from django_summernote.widgets import SummernoteWidget
from django.conf import settings
import copy


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "parent":forms.URLInput(
                attrs = {
                    "type":"hidden",
                }
            ),
        }
