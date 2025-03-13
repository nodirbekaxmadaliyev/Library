from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from books.models import Book
from pupils.models import Pupil
from django.http import JsonResponse

# Create your views here.
class HomePageView(ListView):
    model = Book
    template_name = 'give_book/home.html'

def search_pupil(request, pk):
    if request.method == "POST":
        pupil_id = request.POST.get('pupil_id')
        pupil = Pupil.objects.get(id=pupil_id)
        book = Book.objects.get(pk=pk)
        pupil.books.append(book.name)
        book.number -= 1
        book.save()
        pupil.save()
        return redirect('give_book')


