from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import (Service, Feature, Branch, MeetingRoom, Event, GalleryImage, FAQ, Contact, VisitRequest, BusinessRegistration, Referral)
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BusinessRegistrationForm, VisitRequestForm
from django.db.models import Q

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
    form_class = VisitRequestForm
    template_name = "visits/register.html"
    success_url = reverse_lazy("visit_success")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def visit_success(request):
    return render(request, "visits/success.html")

# create referral
class ReferralCreateView(LoginRequiredMixin, CreateView):
    model = Referral
    fields = ['full_name', 'email', 'phone', 'referred_company']
    template_name = "referrals/register.html"
    success_url = reverse_lazy("referral_success")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def referral_success(request):
    return render(request, "referrals/success.html")

# business
# create
class BusinessRegistrationCreateView(LoginRequiredMixin, CreateView):
    model = BusinessRegistration
    form_class = BusinessRegistrationForm
    template_name = "business/register.html"
    success_url = reverse_lazy("business_success")

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, "business"):
            return redirect("business_success")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def business_success(request):
    return render(request, "business/success.html")

# search bar
def search(request):
    query = request.GET.get("q", "").strip()

    services = Service.objects.none()
    rooms = MeetingRoom.objects.none()
    faqs = FAQ.objects.none()

    if query:
        services = Service.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        rooms = MeetingRoom.objects.filter(
            Q(name__icontains=query) |
            Q(branch__name__icontains=query)
        )

        faqs = FAQ.objects.filter(
            Q(question__icontains=query) |
            Q(answer__icontains=query)
        )

    context = {
        "query": query,
        "services": services,
        "rooms": rooms,
        "faqs": faqs,
    }

    return render(request, "search/results.html", context)

# signup
def signup(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("business_register")

    return render(
        request,
        "registration/signup.html",
        {"form": form},
    )