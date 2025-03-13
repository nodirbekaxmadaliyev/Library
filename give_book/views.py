from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from pupils.models import Pupil
from django.http import JsonResponse

# Create your views here.
class HomePageView(ListView):
    model = Book
    template_name = 'give_book/home.html'

class GiveBookView(DetailView):
    model = Book
    template_name = 'give_book/give_book.html'


def search_student(request):
    if request.method == "GET":
        student_id = request.GET.get('student_id')
        try:
            # student_id ni int ga aylantirish xavfsizlik uchun yaxshi amaliyot
            student_id = int(student_id)

            # student_id o'rniga id dan foydalaniladi
            student = Pupil.objects.get(id=student_id)
            return JsonResponse({'name': f"{student.first_name} {student.last_name}"})
        except Pupil.DoesNotExist:
            return JsonResponse({'error': 'Talaba topilmadi'})
        except ValueError:
            return JsonResponse({'error': 'Noto‘g‘ri ID format'})


def kitob_berish(request):
    if request.method == "POST":
        student_id = request.POST.get("studentId")
        bookName = request.POST.get("bookId")

        pupil = Pupil.objects.get(id=student_id)
        pupil.books.append(bookName)
        pupil.save()

        book = Book.objects.get(name=bookName)
        book.number -= 1
        book.save()

        if student_id:
            return JsonResponse({"success": True, "message": "Kitob berildi!"})
        else:
            return JsonResponse({"success": False, "message": "Talaba ID kiritilmagan!"})

@login_required
def profile_view(request):
    return render(request, 'give_book/user_detail.html', {'user': request.user})
