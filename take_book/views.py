from django.views.generic import ListView
from pupils.models import Pupil
from django.http import HttpResponse
from django.shortcuts import redirect, render
from books.models import Book
from django.contrib import messages

# Create your views here.
class HomePageView(ListView):
    model = Pupil
    template_name = 'take_book/home.html'

    def get_queryset(self):
        queryset = Pupil.objects.all()
        id_q = self.request.GET.get("id", "").strip()
        first_name_q = self.request.GET.get("first_name", "").strip()
        last_name_q = self.request.GET.get("last_name", "").strip()
        group_q = self.request.GET.get("group", "").strip()
        course_q = self.request.GET.get("course", "").strip()
        books_q = self.request.GET.get("books", "").strip()

        if id_q:
            queryset = queryset.filter(id__icontains=id_q)
        if first_name_q:
            queryset = queryset.filter(first_name__icontains=first_name_q)
        if last_name_q:
            queryset = queryset.filter(last_name__icontains=last_name_q)
        if group_q:
            queryset = queryset.filter(group__icontains=group_q)
        if course_q:
            queryset = queryset.filter(course__icontains=course_q)
        if books_q:
            queryset = queryset.filter(books__icontains=books_q)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(self.request, "take_book/home.html", context)
        return super().render_to_response(context, **response_kwargs)


def select_book(request, pk1):
        selected_books = request.POST.getlist('selected_books[]')
        pupil = Pupil.objects.get(pk=pk1)
        for sbook in selected_books:
            pupil.books.remove(sbook)
            book = Book.objects.filter(name=sbook).first()
            book.number += 1
            book.save()
        pupil.save()
        return redirect('take_book')
