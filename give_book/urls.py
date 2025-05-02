from django.urls import path
from .views import HomePageView, recognize_face, search_pupil

urlpatterns = [
    path('', HomePageView.as_view(), name='give_book'),
    path('api/recognize_face/', recognize_face, name='recognize_face'),
    path('search_pupil/<int:pk>/', search_pupil, name='search_pupil'),
]