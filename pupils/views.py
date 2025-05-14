from django.core.exceptions import ValidationError
from django.core.serializers import json
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .forms import ExcelUploadForm
import pandas as pd
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Pupil
from .forms import PupilForm
import json
import base64
import cv2
import numpy as np
from django.core.files.base import ContentFile
# Create your views here.

class PupilsListView(ListView, FormView):
    model = Pupil
    template_name = "pupil/pupils.html"

    form_class = ExcelUploadForm  # Fayl yuklash formasi
    success_url = reverse_lazy("pupils")

    def get_queryset(self):
        queryset = Pupil.objects.all()

        # Qidiruv parametrlari
        id_q = self.request.GET.get("id", "").strip()
        first_name_q = self.request.GET.get("first_name", "").strip()
        last_name_q = self.request.GET.get("last_name", "").strip()
        group_q = self.request.GET.get("group", "").strip()
        course_q = self.request.GET.get("course", "").strip()
        books_q = self.request.GET.get("books", "").strip()

        # Filtr qo‘llash
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

    def form_valid(self, form):
        message = None
        try:
            excel_file = self.request.FILES["excel_file"]
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Pupil.objects.create(
                    first_name=row['Ismi'],
                    last_name=row['Familiyasi'],
                    group=row['Guruhi'],
                    course=row['Kursi']
                )

            message = "Fayl muvaffaqiyatli yuklandi!"
        except Exception as e:
            message = f"Xatolik yuz berdi. Excel faylni tekshirib ko‘ring. ({str(e)})"

        return render(self.request, self.template_name, {
            "form": form,
            "students": Pupil.objects.all(),
            "message": message
        })

    def render_to_response(self, context, **response_kwargs):
        # AJAX so‘rov bo‘lsa, faqat jadvalni qaytarish
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(self.request, "pupil/pupils.html", context)
        return super().render_to_response(context, **response_kwargs)


class PupilCreateView(CreateView):
    model = Pupil
    form_class = PupilForm
    template_name = 'pupil/pupil_add.html'
    success_url = reverse_lazy('pupils')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # AJAX so'rov bo'lsa (yuzni tanib olish)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'recognize_face' in request.path:
            return self.recognize_face(request)

        # Oddiy POST so'rov bo'lsa (talabani saqlash)
        return super().post(request, *args, **kwargs)

    def recognize_face(self, request):
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]  # Remove data:image/png;base64,
            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 0:
                return JsonResponse({'success': False, 'message': 'Yuz aniqlanmadi!'})

            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (100, 100))
            captured_encoding = face_roi.tobytes()

            # Bazadagi barcha talabalarning yuz kodlari bilan solishtirish
            pupils = Pupil.objects.exclude(face_encoding__isnull=True)
            for pupil in pupils:
                if pupil.face_encoding:
                    stored_encoding = np.frombuffer(pupil.face_encoding, dtype=np.uint8)
                    stored_encoding = stored_encoding.reshape(100, 100)

                    # Oddiy solishtirish
                    difference = cv2.absdiff(stored_encoding, face_roi)
                    similarity = 1 - (np.sum(difference) / (100 * 100 * 255))

                    if similarity > 0.8:  # 80% o'xshashlik
                        return JsonResponse({
                            'success': True,
                            'pupil': {
                                'first_name': pupil.first_name,
                                'last_name': pupil.last_name,
                                'group': pupil.group,
                                'course': pupil.course
                            },
                            'message': 'Bu foydalanuvchi allaqachon mavjud'
                        })

            return JsonResponse({'success': False, 'message': 'Yangi foydalanuvchi'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    def form_valid(self, form):
        try:
            form.instance.full_clean()  # Model validatsiyasini ishga tushiramiz
            return super().form_valid(form)
        except ValidationError as e:
            return self.form_invalid(form)

    def form_invalid(self, form):
        errors = {f: e.get_json_data() for f, e in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors})

@csrf_exempt
def recognize_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            if len(faces) == 0:
                return JsonResponse({'success': False, 'message': 'Yuz aniqlanmadi!'})

            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]
            face_roi = cv2.resize(face_roi, (100, 100))

            # Bazadagi barcha talabalarni solishtirish
            pupils = Pupil.objects.exclude(face_encoding__isnull=True)
            for pupil in pupils:
                if pupil.face_encoding:
                    stored_encoding = np.frombuffer(pupil.face_encoding, dtype=np.uint8).reshape(100, 100)
                    difference = cv2.absdiff(stored_encoding, face_roi)
                    similarity = 1 - (np.sum(difference) / (100 * 100 * 255))

                    if similarity > 0.5:
                        return JsonResponse({
                            'success': True,
                            'pupil': {
                                'first_name': pupil.first_name,
                                'last_name': pupil.last_name
                            }
                        })

            return JsonResponse({'success': False, 'message': 'Yuz bazada topilmadi!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Noto\'g\'ri so\'rov'})


class PupilDetailView(DetailView):
    model = Pupil
    template_name = 'pupil/pupil_detail.html'

class PupilUpdateView(UpdateView):
    model = Pupil
    fields = ['first_name', 'last_name', 'group', 'course']
    template_name = 'pupil/pupil_update.html'
    def get_success_url(self):
        return reverse_lazy('pupil_detail', args=[self.object.pk])

class PupilDeleteView(DeleteView):
    model = Pupil
    template_name = 'pupil/pupil_delete.html'
    success_url = reverse_lazy('pupils')


