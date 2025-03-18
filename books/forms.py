from django.forms import ModelForm
from .models import Book
from django import forms

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_code', 'name', 'authors', 'year', 'book_lang', 'number']

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()