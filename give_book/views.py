from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from books.models import Book
from pupils.models import Pupil
from django.http import JsonResponse
# Create your views here.
class HomePageView(ListView):
    model = Book
    template_name = 'give_book/home.html'

    def get_queryset(self):
        queryset = Book.objects.all()

        # Qidiruv parametrlari
        code_q = self.request.GET.get("code", "").strip()
        name_q = self.request.GET.get("name", "").strip()
        author_q = self.request.GET.get("author", "").strip()
        year_q = self.request.GET.get("year", "").strip()
        language_q = self.request.GET.get("language", "").strip()
        number_q = self.request.GET.get("number", "").strip()

        # Filtr qo‘llash
        if code_q:
            queryset = queryset.filter(book_code__icontains=code_q)
        if name_q:
            queryset = queryset.filter(name__icontains=name_q)
        if author_q:
            queryset = queryset.filter(authors__icontains=author_q)
        if year_q:
            queryset = queryset.filter(year__icontains=year_q)
        if language_q:
            queryset = queryset.filter(book_lang__icontains=language_q)
        if number_q:
            queryset = queryset.filter(number__icontains=number_q)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # AJAX so‘rov bo‘lsa, faqat jadvalni qaytarish
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(self.request, "give_book/home.html", context)
        return super().render_to_response(context, **response_kwargs)


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


def check_pupil(request, pupil_id):
    from django.http import JsonResponse
    try:
        pupil = Pupil.objects.get(id=pupil_id)
        return JsonResponse({"exists": True, "first_name": f"{pupil.last_name} {pupil.first_name}"})
    except Pupil.DoesNotExist:
        return JsonResponse({"exists": False})


