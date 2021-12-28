from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import SelectMultiple, TextInput, Textarea, EmailInput, CheckboxInput,URLInput, Select, NumberInput, RadioSelect, FileInput
from apis.models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('timestamp',)
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','id':'name', 'placeholder': 'Name'}),
            'title': TextInput(attrs={'class': 'required form-control','id':'title', 'placeholder': 'Title'}),
            'description': TextInput(attrs={'class': 'required form-control','id':'description', 'placeholder': 'Description'}),
        }


