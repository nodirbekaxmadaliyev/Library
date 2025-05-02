from django.views.generic import ListView
from django.shortcuts import redirect, render
from books.models import Book
import base64
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pupils.models import Pupil
import json

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

@csrf_exempt
def face_match_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        img_data = data.get('image', '').split(',')[1]
        img_bytes = base64.b64decode(img_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 5)

        if len(faces) == 0:
            return JsonResponse({'success': False})

        (x, y, w, h) = faces[0]
        face_roi = img[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, (100, 100))

        for pupil in Pupil.objects.exclude(face_encoding=None):
            stored_encoding = np.frombuffer(pupil.face_encoding, dtype=np.uint8)
            stored_encoding = stored_encoding.reshape(100, 100)
            diff = cv2.absdiff(stored_encoding, face_roi)
            similarity = 1 - (np.sum(diff) / (100 * 100 * 255))
            if similarity > 0.5:
                return JsonResponse({'success': True, 'pupil_id': pupil.pk})
        return JsonResponse({'success': False})
    return JsonResponse({'success': False})
