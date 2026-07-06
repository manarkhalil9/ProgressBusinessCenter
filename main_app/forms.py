from django import forms
from .models import BusinessRegistration, VisitRequest


class BusinessRegistrationForm(forms.ModelForm):

    class Meta:
        model = BusinessRegistration

        fields = [
            "company_name",
            "owner_name",
            "commercial_registration",
            "business_type",
            "services",
        ]

        widgets = {
            "services": forms.CheckboxSelectMultiple(),
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

        widgets = {
            'preferred_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'preferred_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
        }