# main_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import (
    Service, Feature, Branch, MeetingRoom, Event, GalleryImage,
    FAQ, Contact, VisitRequest, BusinessRegistration, Referral,
    Office, Booking
)
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (
    BusinessRegistrationForm, VisitRequestForm, BookingForm, ReferralForm
)
from django.db.models import Q
from django.http import Http404
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, datetime, timedelta
import calendar


# ---------- HOME ----------
def home(request):
    return render(request, 'index.html')


# ---------- ABOUT ----------
def about(request):
    return render(request, 'about.html')


# ---------- SERVICES ----------
class ServiceList(ListView):
    model = Service
    template_name = 'services/index.html'
    context_object_name = 'services'


class ServiceDetail(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'


# ---------- FEATURES ----------
class FeatureListView(ListView):
    model = Feature
    template_name = 'features/index.html'
    context_object_name = 'features'


class FeatureDetailView(DetailView):
    model = Feature
    template_name = 'features/detail.html'
    context_object_name = 'feature'


# ---------- BRANCHES ----------
class BranchListView(ListView):
    model = Branch
    template_name = 'branches/index.html'
    context_object_name = 'branches'


class BranchDetailView(DetailView):
    model = Branch
    template_name = 'branches/detail.html'
    context_object_name = 'branch'


# ---------- MEETING ROOMS ----------
class MeetingRoomListView(ListView):
    model = MeetingRoom
    template_name = 'rooms/index.html'
    context_object_name = 'rooms'


class MeetingRoomDetailView(DetailView):
    model = MeetingRoom
    template_name = 'rooms/detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


# ---------- OFFICES ----------
class OfficeListView(ListView):
    model = Office
    template_name = "offices/index.html"
    context_object_name = "offices"

    def get_queryset(self):
        return Office.objects.select_related("branch")


class OfficeDetailView(DetailView):
    model = Office
    template_name = "offices/detail.html"
    context_object_name = "office"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context


# ---------- EVENTS ----------
class EventListView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'


# ---------- GALLERY ----------
class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'gallery/index.html'
    context_object_name = 'gallery'


class GalleryDetailView(DetailView):
    model = GalleryImage
    template_name = 'gallery/detail.html'
    context_object_name = 'image'


# ---------- FAQ ----------
class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/index.html'
    context_object_name = 'faqs'


class FAQDetailView(DetailView):
    model = FAQ
    template_name = 'faq/detail.html'
    context_object_name = 'faq'


# ---------- CONTACT ----------
class ContactView(DetailView):
    model = Contact
    template_name = 'contact/detail.html'
    context_object_name = 'contact'

    def get_object(self):
        return Contact.objects.first()


# ---------- VISIT REQUESTS ----------
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


# ---------- REFERRALS ----------
class ReferralCreateView(LoginRequiredMixin, CreateView):
    model = Referral
    form_class = ReferralForm
    template_name = "referrals/index.html"
    success_url = reverse_lazy("referral_success")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def referral_success(request):
    return render(request, "referrals/success.html")


# ---------- BUSINESS REGISTRATION ----------
class BusinessRegistrationCreateView(LoginRequiredMixin, CreateView):
    model = BusinessRegistration
    form_class = BusinessRegistrationForm
    template_name = "business/register.html"
    success_url = reverse_lazy("business_success")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def business_success(request):
    return render(request, 'business/success.html')


# ---------- SEARCH ----------
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


# ---------- BOOKING ----------
# ---------- BOOKING ----------
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/create.html"

    def get_resource(self):
        resource_type = self.kwargs["resource_type"]
        pk = self.kwargs["pk"]

        if resource_type == "room":
            return get_object_or_404(MeetingRoom, pk=pk)

        if resource_type == "office":
            return get_object_or_404(Office, pk=pk)

        raise Http404("Booking item not found.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Attach user and resource BEFORE form.is_valid() runs model clean()
        form.instance.user = self.request.user
        resource = self.get_resource()
        
        if isinstance(resource, MeetingRoom):
            form.instance.meeting_room = resource
        elif isinstance(resource, Office):
            form.instance.office = resource
            
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["resource"] = self.get_resource()
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["client_name"] = (
            self.request.user.get_full_name()
            or self.request.user.username
        )
        initial["email"] = self.request.user.email
        initial["start_date"] = date.today()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        resource = self.get_resource()

        context["resource"] = resource
        context["resource_type"] = self.kwargs["resource_type"]

        selected_date = date.today()

        if self.request.method == "POST":
            date_str = self.request.POST.get("start_date")
            if date_str:
                try:
                    selected_date = datetime.strptime(
                        date_str,
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    pass
        else:
            date_str = self.request.GET.get("date")
            if date_str:
                try:
                    selected_date = datetime.strptime(
                        date_str,
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    pass

        context["selected_date"] = selected_date
        context["today"] = date.today()

        year = selected_date.year
        month = selected_date.month

        cal = calendar.Calendar(firstweekday=6)
        context["month_days"] = cal.monthdatescalendar(year, month)
        context["month_name"] = calendar.month_name[month]
        context["year"] = year

        if isinstance(resource, Office):
            context["unavailable_dates"] = resource.get_unavailable_dates(year, month)
        else:
            context["unavailable_dates"] = set()

        if month == 1:
            prev_month = date(year - 1, 12, 1)
        else:
            prev_month = date(year, month - 1, 1)

        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)

        context["previous_month"] = prev_month.strftime("%Y-%m-%d")
        context["next_month"] = next_month.strftime("%Y-%m-%d")

        if isinstance(resource, MeetingRoom):
            context["available_slots"] = resource.get_available_time_slots(selected_date)
        else:
            context["available_slots"] = None

        return context

    def form_valid(self, form):
        resource = self.get_resource()

        if isinstance(resource, MeetingRoom):
            start_dt = datetime.combine(
                form.cleaned_data["start_date"],
                form.cleaned_data["start_time"],
            )

            end_dt = datetime.combine(
                form.cleaned_data["start_date"],
                form.cleaned_data["end_time"],
            )

            is_free = resource.is_available(start_dt, end_dt)

        else:
            is_free = resource.is_available(
                form.cleaned_data["start_date"],
                form.cleaned_data["end_date"],
            )

        form.instance.status = "approved" if is_free else "pending"

        response = super().form_valid(form)

        booking = self.object

        send_mail(
            subject=f"New Booking Request: {booking.client_name}",
            message=(
                f"Booking for "
                f"{booking.meeting_room or booking.office}\n"
                f"Status: {booking.status}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        if booking.status == "approved":
            subject = "Booking Approved"
            message = (
                f"Your booking for "
                f"{booking.meeting_room or booking.office} "
                f"has been approved.\n\n"
                f"Total Price: {booking.total_price} BHD"
            )
        else:
            subject = "Booking Received"
            message = (
                f"Your booking request for "
                f"{booking.meeting_room or booking.office} "
                f"is currently pending review."
            )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=True,
        )

        return response

    def form_invalid(self, form):
        print("========== BOOKING FORM ERRORS ==========")
        print(form.errors)
        print(form.non_field_errors())
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("booking_success")


def booking_success(request):
    return render(request, "bookings/success.html")

# ---------- CANCEL BOOKING ----------
class BookingCancelView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        return render(request, "bookings/confirm_cancel.html", {"booking": booking})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.status = "cancelled"
        booking.save()
        return redirect("dashboard")

    def test_func(self):
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'])
        return booking.user == self.request.user


# ---------- CANCEL BUSINESS REGISTRATION ----------
class BusinessRegistrationCancelView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        registration = get_object_or_404(BusinessRegistration, pk=pk)
        registration.delete()
        return redirect("dashboard")

    def test_func(self):
        registration = get_object_or_404(BusinessRegistration, pk=self.kwargs['pk'])
        return registration.user == self.request.user


# ---------- USER DASHBOARD ----------
class UserDashboardView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "dashboard/index.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (
            Booking.objects.filter(user=self.request.user)
            .select_related("meeting_room", "office")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["corporate_registrations"] = (
            BusinessRegistration.objects.filter(user=self.request.user)
            .order_by("-submitted_at")
        )

        return context

# ---------- SIGNUP ----------
def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("business_register")
    return render(request, "registration/signup.html", {"form": form})