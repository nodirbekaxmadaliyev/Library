from django import forms
from django.core.exceptions import ValidationError

from .models import Pupil

class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ['first_name', 'last_name', 'group', 'course', 'face_image']

    def clean(self):
        cleaned_data = super().clean()
        instance = Pupil(**cleaned_data)
        try:
            instance.clean()
        except ValidationError as e:
            self.add_error(None, e)
        return cleaned_data

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()