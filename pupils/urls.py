from django.urls import path
from . import views

urlpatterns = [
    path('', views.PupilsListView.as_view(), name='pupils'),
    path('<int:pk>/', views.PupilDetailView.as_view(), name='pupil_detail'),
    path('<int:pk>/update/', views.PupilUpdateView.as_view(), name='pupil_update'),
    path('<int:pk>/delete/', views.PupilDeleteView.as_view(), name='pupil_delete'),
    path('add/', views.PupilCreateView.as_view(), name='pupil_add'),
    path('recognize-face/', views.PupilCreateView.as_view(), name='recognize_face'),
]