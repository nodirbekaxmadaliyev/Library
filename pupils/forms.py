from django.forms import ModelForm
from .models import Pupil
from django import forms

class PupilForm(ModelForm):
    class Meta:
        model = Pupil
        fields = ['first_name', 'last_name', 'group', 'course']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

