from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import (Service, Feature, Branch, MeetingRoom, Event, GalleryImage, FAQ, ContactMessage, VisitRequest, BusinessRegistration, Referral)
from django.urls import reverse_lazy

# Create your views here.

# home page
def home(request):
    return render(request, 'index.html')

#about page
def about(request):
    return render(request, 'about.html')

#services
#list 
class ServiceList(ListView):
    model = Service
    template_name = 'services/index.html'
    context_object_name = 'services'

# detail
class ServiceDetail(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'

# create
class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('services')

# update
class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('services')

# delete
class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('services')

# features
# list
class FeatureListView(ListView):
    model = Feature
    template_name = 'features/index.html'

# detail
class FeatureDetailView(DetailView):
    model = Feature
    template_name = 'features/detail.html'

# create
class FeatureCreateView(CreateView):
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('features')

# update
class FeatureUpdateView(UpdateView):
    model = Feature
    fields = '__all__'
    success_url = reverse_lazy('features')

# delete
class FeatureDeleteView(DeleteView):
    model = Feature
    success_url = reverse_lazy('features')

# branches
class BranchListView(ListView):
    model = Branch
    template_name = 'branches/index.html'

class BranchDetailView(DetailView):
    model = Branch
    template_name = 'branches/detail.html'

class BranchCreateView(CreateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branches')

class BranchUpdateView(UpdateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branches')

class BranchDeleteView(DeleteView):
    model = Branch
    success_url = reverse_lazy('branches')