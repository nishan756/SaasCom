from .models import Report
from django import forms 

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["report_type","reason"]
        widgets = {
            "report_type" : forms.Select(
                attrs = {
                    "class":"form-select",
                    "required":True
                }
            ),
            "reason":forms.Textarea(
                attrs = {
                    "class":"form-control",
                    "placeholder":"Reason for reporting",
                    "rows":5,
                }
            )
        }