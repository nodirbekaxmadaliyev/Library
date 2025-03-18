from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from .forms import PupilForm, ExcelUploadForm
from .models import Pupil
import pandas as pd
# Create your views here.

class PupilsListView(ListView, FormView):
    model = Pupil  # ListView uchun model
    template_name = "pupil/pupils.html"

    form_class = ExcelUploadForm  # Fayl yuklash formasi
    success_url = reverse_lazy("pupils")  # Fayl yuklanganidan keyin qaytish yo‘li

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
        except:
            message = f"Xatolik yuz berdi. Excel faylni tekshirib ko`ring."

        return render(self.request, self.template_name, {
            "form": form,
            "students": Pupil.objects.all(),
            "message": message
        })


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


