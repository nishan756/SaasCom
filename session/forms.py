from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()

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

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "first_name", 
            "last_name", 
            "username", 
            "email", 
            "user_type", 
            "gender", 
            "date_of_birth", 
            "image", 
            "bio"
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3 , "placeholder":"Bio"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, (forms.Select, forms.RadioSelect)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control' , "placeholder":field_name.capitalize()})

class EditProfileForm(forms.ModelForm):
    class Meta(SignUpForm.Meta):
        model = User
        fields = ["username" ,"first_name" , "last_name" , "bio" , "image" , "gender" , "email"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, (forms.Select, forms.RadioSelect)):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control' , "placeholder":field_name.capitalize()})

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control' , "placeholder":field_name.capitalize()})
