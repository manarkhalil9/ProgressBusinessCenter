from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services_index, name='services_index'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
]