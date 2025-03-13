from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Book
from .forms import BookForm

class BooksListView(ListView):
    model = Book
    template_name = 'book/books.html'

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
