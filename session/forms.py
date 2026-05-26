from django import forms

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
