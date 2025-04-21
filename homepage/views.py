from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'homepage/homepage.html'
    def get(self, request, *args, **kwargs):
        # Shartni tekshirish (masalan, foydalanuvchi autentifikatsiyadan o‘tganmi?)
        if not request.user.is_authenticated:
            # Agar shart bajarilsa, foydalanuvchini boshqa URL'ga yo‘naltiramiz
            return redirect('login')  # yoki '/login/' (login sahifangizga)

        # Agar shart bajarilmasa, asl sahifani qaytaramiz
        return super().get(request, *args, **kwargs)


def profile_view(request):
    return render(request, 'homepage/user_detail.html', {'user': request.user})