from .models import Job
from django import forms 

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["company"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex:Backend Developer"
            }),

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "job_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "min_salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "20000"
            }),

            "max_salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "50000"
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Dhaka, Bangladesh"
            }),

            "deadline": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local"
            }),
        }