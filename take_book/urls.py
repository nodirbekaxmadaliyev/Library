from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'take_book'),
    path('select_book/<int:pk>/', views.select_book, name='select_book'),
]