from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksListView.as_view(), name = 'books'),
    path('add/', views.BookCreateView.as_view(), name = 'book_add'),
    path('<int:pk>/', views.BookDetailView.as_view(), name = 'book_detail'),
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name = 'book_update'),
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name = 'book_delete'),
]