from .models import Job , Application
from django import forms 

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ["user" , "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex:Backend Developer"
            }),

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "skills": forms.SelectMultiple(attrs={
                "class": 'form-control',
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
            "experience": forms.Select(attrs={
                "class": "form-select",
            }),
            "vacancy": forms.NumberInput(attrs={
                "class": "form-control",
            }),
            "currency": forms.Select(attrs={
                "class": "form-select",
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ["job" , "user" , "applied_at" , "hr_message" , "status"]
        widgets = {
            "cover_letter": forms.FileInput(attrs={
                "class": "form-control",
            }),
            "resume": forms.FileInput(attrs={
                "class": "form-control",
            }),
            
        }