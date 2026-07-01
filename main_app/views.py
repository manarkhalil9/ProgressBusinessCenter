from django.shortcuts import render
from .models import Service

# Create your views here.


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services_index(request):
    services = Service.objects.all()

    return render(request, 'services/index.html', {'services':services})