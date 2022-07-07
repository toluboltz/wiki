from turtle import width
from django import forms
from django.core.exceptions import ValidationError
from . import util


# Ensure title does not exist
def validate_title(title):
    if util.get_entry(title.strip()):
        raise ValidationError("Entry exists with the provided title")


class NewPageForm(forms.Form):
    title = forms.CharField(validators=[validate_title], widget=forms.TextInput(attrs={
        "placeholder": "Title", 
        "class": "form-control", 
        "style": "width: 200px;"
        }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Create a New Page using Markdown",
        "class": "form-control"
        }))


class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control"
    }))