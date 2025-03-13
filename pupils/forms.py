from django.forms import ModelForm
from .models import Pupil

class PupilForm(ModelForm):
    class Meta:
        model = Pupil
        fields = ['first_name', 'last_name', 'group', 'course']

