from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'give_book'),
   # path('kitob-berish/', views.kitob_berish, name='kitob_berish'),
    path('search-pupil/<int:pk>/', views.search_pupil, name='search_pupil'),

]