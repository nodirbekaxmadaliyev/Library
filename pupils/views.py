from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import PupilForm
from .models import Pupil
# Create your views here.

class PupilsListView(ListView):
    model = Pupil
    template_name = 'pupil/pupils.html'

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


