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
    template_name = 'form.html'
    success_url = reverse_lazy('services_index')

# update
class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('services_index')

# delete
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('services_index')

# features
# list
class FeatureListView(ListView):
    model = Feature
    template_name = 'features/index.html'
    context_object_name = 'features'

# detail
class FeatureDetailView(DetailView):
    model = Feature
    template_name = 'features/detail.html'
    context_object_name = 'feature'

# create
class FeatureCreateView(CreateView):
    model = Feature
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('features')

# update
class FeatureUpdateView(UpdateView):
    model = Feature
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('features')

# delete
class FeatureDeleteView(DeleteView):
    model = Feature
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('features')

# branches
# list
class BranchListView(ListView):
    model = Branch
    template_name = 'branches/index.html'
    context_object_name = 'branches'

# detail
class BranchDetailView(DetailView):
    model = Branch
    template_name = 'branches/detail.html'
    context_object_name = 'branch'

# create
class BranchCreateView(CreateView):
    model = Branch
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('branches')

# update
class BranchUpdateView(UpdateView):
    model = Branch
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('branches')

# delete
class BranchDeleteView(DeleteView):
    model = Branch
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('branches')

# meeting rooms
# list
class MeetingRoomListView(ListView):
    model = MeetingRoom
    template_name = 'rooms/index.html'
    context_object_name = 'rooms'

# detail
class MeetingRoomDetailView(DetailView):
    model = MeetingRoom
    template_name = 'rooms/detail.html'
    context_object_name = 'room'

# create
class MeetingRoomCreateView(CreateView):
    model = MeetingRoom
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('rooms')

# update
class MeetingRoomUpdateView(UpdateView):
    model = MeetingRoom
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('rooms')

# delete
class MeetingRoomDeleteView(DeleteView):
    model = MeetingRoom
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('rooms')

# events
# list
class EventListView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'

# detail
class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

# create
class EventCreateView(CreateView):
    model = Event
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('events')

# update
class EventUpdateView(UpdateView):
    model = Event
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('events')

# delete
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('events')

# gallery
# list
class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/index.html'
    context_object_name = 'gallery'

# detail
class GalleryDetailView(DetailView):
    model = GalleryImage
    template_name = 'gallery/detail.html'
    context_object_name = 'image'

# FAQ
# list
class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/index.html'
    context_object_name = 'faqs'

# detail
class FAQDetailView(DetailView):
    model = FAQ
    template_name = 'faq/detail.html'
    context_object_name = 'faq'

# contact, visit, referral
# create
class ContactCreateView(CreateView):
    model = ContactMessage
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('home')

class VisitCreateView(CreateView):
    model = VisitRequest
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('home')

class ReferralCreateView(CreateView):
    model = Referral
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('home')

# business
# list
class BusinessListView(ListView):
    model = BusinessRegistration
    template_name = 'business/index.html'
    context_object_name = 'businesses'

# detail
class BusinessDetailView(DetailView):
    model = BusinessRegistration
    template_name = 'business/detail.html'
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['services'] = Service.objects.exclude(
            id__in=self.object.services.all()
        )

        return context

# many to many 'business - services'
def add_service(request, business_id, service_id):
    business = get_object_or_404(BusinessRegistration, id=business_id)
    business.services.add(service_id)
    return redirect('business_detail', pk=business_id)


def remove_service(request, business_id, service_id):
    business = get_object_or_404(BusinessRegistration, id=business_id)
    business.services.remove(service_id)
    return redirect('business_detail', pk=business_id)