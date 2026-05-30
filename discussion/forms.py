from .models import Discussion
from django import forms 


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        exclude = ["author"]
    
    def __init__(self, *args , **kwargs):
        super().__init__(*args , **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class":"form-control",
                "placeholder":field.title
            })
