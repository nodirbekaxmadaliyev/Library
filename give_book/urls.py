from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'home'),
    path('give/<int:pk>/', views.GiveBookView.as_view(), name = 'give_book'),
    path('kitob-berish/', views.kitob_berish, name='kitob_berish'),
    path('search/', views.search_student, name='search_student'),
    path('profile/', views.profile_view, name='profile'),
]