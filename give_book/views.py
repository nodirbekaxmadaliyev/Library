from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import cv2
import numpy as np
import base64
from books.models import Book
from pupils.models import Pupil


class HomePageView(ListView):
    model = Book
    template_name = 'give_book/home.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.all()
        # Qidiruv parametrlari
        code_q = self.request.GET.get("code", "").strip()
        name_q = self.request.GET.get("name", "").strip()
        author_q = self.request.GET.get("author", "").strip()
        year_q = self.request.GET.get("year", "").strip()
        language_q = self.request.GET.get("language", "").strip()
        number_q = self.request.GET.get("number", "").strip()

        # Filtr qo'llash
        if code_q: queryset = queryset.filter(book_code__icontains=code_q)
        if name_q: queryset = queryset.filter(name__icontains=name_q)
        if author_q: queryset = queryset.filter(authors__icontains=author_q)
        if year_q: queryset = queryset.filter(year__icontains=year_q)
        if language_q: queryset = queryset.filter(book_lang__icontains=language_q)
        if number_q: queryset = queryset.filter(number__icontains=number_q)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(self.request, "give_book/home.html", context)
        return super().render_to_response(context, **response_kwargs)


def search_pupil(request, pk):
    if request.method == "POST":
        pupil_id = request.POST.get('pupil_id')
        pupil = get_object_or_404(Pupil, id=pupil_id)
        book = get_object_or_404(Book, pk=pk)

        # Kitob sonini tekshirish
        if book.number <= 0:
            return JsonResponse({'success': False, 'message': 'Bu kitobdan qolmagan'})

        # Talaba allaqachon bu kitobni olganmi?
        if book.name in pupil.books:
            return JsonResponse({'success': False, 'message': 'Talaba bu kitobni allaqachon olgan'})

        # Kitob sonini kamaytirish
        book.number -= 1
        book.save()

        # Talabaga kitobni qo'shish
        pupil.books.append(book.name)
        pupil.save()

        return JsonResponse({'success': True, 'message': 'Kitob muvaffaqiyatli topshirildi'})
    return JsonResponse({'success': False, 'message': 'Faqat POST so\'rovlari qabul qilinadi'})


@csrf_exempt
def recognize_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image', '').split(',')[1]

            # Rasmni qayta ishlash
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Yuzni aniqlash
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                return JsonResponse({'success': False, 'message': 'Yuz aniqlanmadi'})

            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (100, 100))

            # Bazadagi talabalarni solishtirish
            for pupil in Pupil.objects.all():
                if pupil.face_encoding:
                    stored_encoding = np.frombuffer(pupil.face_encoding, dtype=np.uint8)
                    stored_encoding = stored_encoding.reshape(100, 100)

                    difference = cv2.absdiff(stored_encoding, face_roi)
                    similarity = 1 - (np.sum(difference) / (100 * 100 * 255))

                    if similarity > 0.9:
                        return JsonResponse({
                            'success': True,
                            'pupil': {
                                'id': pupil.id,
                                'first_name': pupil.first_name,
                                'last_name': pupil.last_name,
                                'group': pupil.group,
                                'course': pupil.course
                            }
                        })

            return JsonResponse({'success': False, 'message': 'Talaba topilmadi'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Faqat POST so\'rovlari qabul qilinadi'})