from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'homepage/homepage.html'


@login_required
def profile_view(request):
    return render(request, 'homepage/user_detail.html', {'user': request.user})