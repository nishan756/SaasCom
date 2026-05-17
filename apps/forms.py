from .models import Review , App
from django import forms 
from cloudinary.forms import CloudinaryJsFileField


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


class AppForm(forms.ModelForm):

    class Meta:
        model = App

        fields = [
            "name",
            "category",
            "tags",
            "logo",
            "short_description",
            "detail"
        ]

        widgets = {

            "name": forms.TextInput(
                attrs = {
                    "placeholder": "App name",
                    "class": "form-control"
                }
            ),

            "category": forms.SelectMultiple(
                attrs = {
                    "class": "form-control"
                }
            ),

            "tags": forms.SelectMultiple(
                attrs = {
                    "class": "form-control"
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs = {
                    "class": "form-control"
                }
            ),

            "short_description": forms.TextInput(
                attrs = {
                    "placeholder": "Short description",
                    "class": "form-control"
                }
            ),

            "detail": forms.Textarea(
                attrs = {
                    "class": "form-control",
                    "rows": 6
                }
            )
        }

        def validate_name(self):
            name = self.cleaned_data.get("name")
            if App.objects.filter(name__iexact = name).exists():
                raise forms.ValidationError("App with this name already exists")

class AppDeletionConfirmationForm(forms.Form):
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control",
                "placeholder":"Enter your password",
            }
        ),
        required = True,
        label = "Password",
        label_suffix = ""
    )