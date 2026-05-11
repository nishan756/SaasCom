from .models import Review
from django import forms 


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
        widgets = {
            "review":forms.Textarea(
                attrs = {
                    "placeholder":"Write your review here...",
                    "class":"form-control comment-input",
                    "rows":5
                }
            )
        }
