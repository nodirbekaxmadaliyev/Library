from django.forms import ModelForm

from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_code', 'name', 'authors', 'year', 'book_lang', 'number']
