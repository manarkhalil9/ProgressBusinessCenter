from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.ServiceList.as_view(), name='services_index'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),
]