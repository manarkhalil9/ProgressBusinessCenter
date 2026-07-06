from django import forms
from .models import BusinessRegistration


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