from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import (Service, Feature, Branch, MeetingRoom, Event, GalleryImage, FAQ, Contact, VisitRequest, BusinessRegistration, Referral)
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

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

# contact detail
class ContactView(DetailView):
    model = Contact
    template_name = 'contact/detail.html'
    context_object_name = 'contact'

    def get_object(self):
        return Contact.objects.first()

# create visit
class VisitCreateView(LoginRequiredMixin, CreateView):
    model = VisitRequest
    fields = ['full_name', 'email', 'phone', 'preferred_date', 'preferred_time', 'notes']
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# create referral
class ReferralCreateView(LoginRequiredMixin, CreateView):
    model = Referral
    fields = ['full_name', 'email', 'phone', 'referred_company']
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# business
# detail
class BusinessDetailView(LoginRequiredMixin, DetailView):
    model = BusinessRegistration
    template_name = 'business/detail.html'
    context_object_name = 'business'

    def get_object(self):
        return BusinessRegistration.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_services'] = Service.objects.exclude(
            id__in=self.object.services.all()
        )
        return context

# create
# class BusinessCreateView(LoginRequiredMixin, CreateView):
#     model = BusinessRegistration
#     fields = ['company_name', 'owner_name', 'commercial_registration', 'business_type', 'services']
#     template_name = 'form.html'
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
    
# add service
def add_service(request, service_id):
    business = get_object_or_404(BusinessRegistration, user=request.user)
    business.services.add(service_id)
    return redirect('business_detail')


# remove service
def remove_service(request, service_id):
    business = get_object_or_404(BusinessRegistration, user=request.user)
    business.services.remove(service_id)
    return redirect('business_detail')

# signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # auto create business profile
            BusinessRegistration.objects.create(user=user)

            login(request, user)
            return redirect('business_detail')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})