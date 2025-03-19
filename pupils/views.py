from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .forms import PupilForm, ExcelUploadForm
from .models import Pupil
import pandas as pd
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


