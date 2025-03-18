from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .models import Book
from .forms import BookForm, ExcelUploadForm
import pandas as pd

class BooksListView(ListView, FormView):
    model = Book
    template_name = 'book/books.html'
    context_object_name = "Books"
    form_class = ExcelUploadForm  # Fayl yuklash formasi
    success_url = reverse_lazy('home')  # Fayl yuklanganidan keyin qaytish yo‘li

    def form_valid(self, form):
        message = None
        try:
            excel_file = self.request.FILES["excel_file"]
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Book.objects.create(
                    book_code=row['Kodi'],
                    name=row['Nomi'],
                    authors=row['Yozuvchilari'],
                    year=row['Yili'],
                    book_lang=row['Tili'],
                    number=row['Soni']
                )

            message = "Fayl muvaffaqiyatli yuklandi!"
        except:
            message = "Xatolik yuz berdi. Excel faylni tekshirib ko`ring."

        return render(self.request, self.template_name, {
            "form": form,
            "Books": Book.objects.all(),
            "message": message
        })


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_add.html'
    success_url = reverse_lazy('books')

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'

class BookUpdateView(UpdateView):
    model = Book
    fields = ['book_code', 'name', 'authors', 'year', 'book_lang', 'number']
    template_name = 'book/book_update.html'

    def get_success_url(self):
        return reverse_lazy('book_detail', args=[self.object.pk])

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('books')
