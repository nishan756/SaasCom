from django import forms
from .models import Report


class LoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        label_suffix = "",
        widget = forms.TextInput(
            attrs = {
                "type":"text",
                "placeholder":"Username",
                "class":"form-control"
            }
        )
    )

    password = forms.CharField(
        required = True,
        label_suffix = "",
        widget = forms.PasswordInput(
            attrs = {
                "type":"password",
                "placeholder":"Password",
                "class":"form-control"
            }
        )
    )


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