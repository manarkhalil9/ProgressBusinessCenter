from django.shortcuts import render, redirect, get_object_or_404
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
# list
class BranchListView(ListView):
    model = Branch
    template_name = 'branches/index.html'

# detail
class BranchDetailView(DetailView):
    model = Branch
    template_name = 'branches/detail.html'

# create
class BranchCreateView(CreateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branches')

# update
class BranchUpdateView(UpdateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branches')

# delete
class BranchDeleteView(DeleteView):
    model = Branch
    success_url = reverse_lazy('branches')

# meeting rooms
# list
class MeetingRoomListView(ListView):
    model = MeetingRoom
    template_name = 'rooms/index.html'

# detail
class MeetingRoomDetailView(DetailView):
    model = MeetingRoom
    template_name = 'rooms/detail.html'

# create
class MeetingRoomCreateView(CreateView):
    model = MeetingRoom
    fields = '__all__'
    success_url = reverse_lazy('rooms')

# update
class MeetingRoomUpdateView(UpdateView):
    model = MeetingRoom
    fields = '__all__'
    success_url = reverse_lazy('rooms')

# delete
class MeetingRoomDeleteView(DeleteView):
    model = MeetingRoom
    success_url = reverse_lazy('rooms')

# events
# list
class EventListView(ListView):
    model = Event
    template_name = 'events/index.html'

# detail
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'

# create
class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    success_url = reverse_lazy('events')

# update
class EventUpdateView(UpdateView):
    model = Event
    fields = '__all__'
    success_url = reverse_lazy('events')

# delete
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('events')

# gallery
# list
class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/index.html'

# detail
class GalleryDetailView(DetailView):
    model = GalleryImage
    template_name = 'gallery/detail.html'

# FAQ
# list
class FAQListView(ListView):
    model = FAQ
    template_name = 'faqs/index.html'

# detail
class FAQDetailView(DetailView):
    model = FAQ
    template_name = 'faqs/detail.html'

# contact, visit, referral
# create
class ContactCreateView(CreateView):
    model = ContactMessage
    fields = '__all__'
    success_url = reverse_lazy('home')

class VisitCreateView(CreateView):
    model = VisitRequest
    fields = '__all__'
    success_url = reverse_lazy('home')

class ReferralCreateView(CreateView):
    model = Referral
    fields = '__all__'
    success_url = reverse_lazy('home')

# business
# list
class BusinessListView(ListView):
    model = BusinessRegistration
    template_name = 'business/index.html'

# detail
class BusinessDetailView(DetailView):
    model = BusinessRegistration
    template_name = 'business/detail.html'

# many to many 'business - services'
def add_service(request, business_id, service_id):
    business = get_object_or_404(BusinessRegistration, id=business_id)
    business.services.add(service_id)
    return redirect('business_detail', pk=business_id)


def remove_service(request, business_id, service_id):
    business = get_object_or_404(BusinessRegistration, id=business_id)
    business.services.remove(service_id)
    return redirect('business_detail', pk=business_id)