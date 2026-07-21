from django import forms
from .models import BusinessRegistration, VisitRequest, Booking, MeetingRoom, Office, Referral
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # Import the translation tool


class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = BusinessRegistration
        fields = [
            "request_type", 
            "company_name",
            "owner_name",
            "commercial_registration",
            "business_type",
            "cpr_number",
            "cpr_document",
            "passport_document",
        ]
        labels = {
            "request_type": _("Request Type"),
            "company_name": _("Company Name"),
            "owner_name": _("Owner Name"),
            "commercial_registration": _("Commercial Registration"),
            "business_type": _("Business Type"),
            "cpr_number": _("CPR Number"),
            "cpr_document": _("Upload CPR"),
            "passport_document": _("Upload Passport"),
        }

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = [
            'full_name',
            'email',
            'phone',
            'preferred_date',
            'preferred_time',
            'notes',
        ]

        labels = {
            "full_name": _("Full Name"),
            "email": _("Email Address"),
            "phone": _("Phone Number"),
            "preferred_date": _("Preferred Date"),
            "preferred_time": _("Preferred Time"),
            "notes": _("Notes"),
        }

        widgets = {
            'preferred_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'preferred_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "client_name",
            "phone",
            "email",
            "commercial_registration",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

        labels = {
            "client_name": _("Client Name"),
            "phone": _("Phone Number"),
            "email": _("Email Address"),
            "commercial_registration": _("Commercial Registration (CR)"),
            "start_date": _("Start Date"),
            "end_date": _("End Date"),
            "start_time": _("Start Time"),
            "end_time": _("End Time"),
        }

    def __init__(self, *args, resource=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = resource

        if isinstance(resource, MeetingRoom):
            self.instance.meeting_room = resource
            self.fields.pop("commercial_registration")
            self.fields.pop("end_date")
            self.fields["start_time"].required = True
            self.fields["end_time"].required = True

        elif isinstance(resource, Office):
            self.instance.office = resource
            self.fields.pop("start_time")
            self.fields.pop("end_time")
            self.fields["commercial_registration"].required = True
            self.fields["end_date"].required = True

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date < date.today():
            # Translate your validation error
            raise ValidationError(_("Please choose today or a future date."))
        return start_date

    def clean(self):
        cleaned_data = super().clean()

        if isinstance(self.resource, MeetingRoom):
            start_time = cleaned_data.get("start_time")
            end_time = cleaned_data.get("end_time")

            if start_time and end_time and end_time <= start_time:
                self.add_error(
                    "end_time",
                    _("End time must be after start time.") # Translate error
                )

        if isinstance(self.resource, Office):
            start_date = cleaned_data.get("start_date")
            end_date = cleaned_data.get("end_date")

            if start_date and end_date and end_date <= start_date:
                self.add_error(
                    "end_date",
                    _("End date must be after start date.") # Translate error
                )

        return cleaned_data
    
class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['full_name', 'email', 'phone', 'referred_company']
        labels = {
            'full_name': _('Full Name'),
            'email': _('Email Address'),
            'phone': _('Phone Number'),
            'referred_company': _('Referred Company Name'),
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': _('Enter full name')}),
            'email': forms.EmailInput(attrs={'placeholder': _('name@example.com')}),
            'phone': forms.TextInput(attrs={'placeholder': _('+973 ...')}),
            'referred_company': forms.TextInput(attrs={'placeholder': _('Enter company name')}),
        }