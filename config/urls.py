from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from give_book import views
from django.views.generic import TemplateView

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('homepage.urls')),
    path('books/', include('books.urls')),
    path('pupils/', include('pupils.urls')),
    path('take_book/', include('take_book.urls')),
    path('give_book/', include('give_book.urls')),
    path('api/check_pupil/<int:pupil_id>/', views.check_pupil, name='check_pupil'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)