from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomePageView.as_view(), name = 'give_book'),
    path('search-pupil/<int:pk>/', views.search_pupil, name='search_pupil'),
    path('api/check_pupil/<int:pupil_id>/', views.check_pupil, name='check_pupil')

]