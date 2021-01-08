from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def dashboard(request):
    context = {

    }

    return render(request, 'engine/dashboard.html', context)
