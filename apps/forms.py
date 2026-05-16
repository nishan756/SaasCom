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

    images = CloudinaryJsFileField(
        attrs = {
            'multiple': True,
            'class': 'form-control',
        },
        options = {
            "folder": "saas_com/assets/images/app_images"
        },
        required = False
    )

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

