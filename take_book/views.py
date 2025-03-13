from django.views.generic import ListView
from pupils.models import Pupil
from django.http import HttpResponse
from django.shortcuts import redirect
from books.models import Book
from django.contrib import messages

# Create your views here.
class HomePageView(ListView):
    model = Pupil
    template_name = 'take_book/home.html'

def select_book(request, pk):
        selected_books = request.POST.getlist('selected_books[]')
        pupil = Pupil.objects.get(pk=pk)
        for sbook in selected_books:
            pupil.books.remove(sbook)
            book = Book.objects.filter(name=sbook).first()
            book.number += 1
            book.save()
        pupil.save()
        return redirect('take_book')
