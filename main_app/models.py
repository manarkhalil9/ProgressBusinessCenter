from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime

# Create your models here.

# services
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
# features
class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    
# branches
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    google_map = models.URLField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# meeting rooms
class MeetingRoom(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='meeting_rooms')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='meeting_rooms/', blank=True, null=True)
    capacity = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=3)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.branch.name}"
    
# office
class Office(models.Model):
    branch = models.ForeignKey( Branch, on_delete=models.CASCADE, related_name='offices')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='offices/', blank=True, null=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=3)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.branch.name}"
    
# booking
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    meeting_room = models.ForeignKey(
        MeetingRoom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="bookings"
    )

    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="bookings"
    )

    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    commercial_registration = models.CharField(max_length=100, blank=True)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        editable=False
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if bool(self.meeting_room) == bool(self.office):
            raise ValidationError(
                "Choose either a meeting room or an office."
            )

        if self.meeting_room:
            if not self.start_time or not self.end_time:
                raise ValidationError(
                    "Start time and end time are required for meeting rooms."
                )

            if self.end_time <= self.start_time:
                raise ValidationError(
                    "End time must be after start time."
                )

        if self.office:
            if not self.end_date:
                raise ValidationError(
                    "End date is required for office bookings."
                )

            if self.end_date <= self.start_date:
                raise ValidationError(
                    "End date must be after start date."
                )

            if not self.commercial_registration:
                raise ValidationError(
                    "CR number is required for office bookings."
                )

    def save(self, *args, **kwargs):
        if self.meeting_room and self.start_time and self.end_time:
            start = datetime.combine(self.start_date, self.start_time)
            end = datetime.combine(self.start_date, self.end_time)

            hours = Decimal(
                str((end - start).total_seconds() / 3600)
            )

            self.total_price = self.meeting_room.price_per_hour * hours

        elif self.office and self.end_date:
            months = (
                (self.end_date.year - self.start_date.year) * 12
                + self.end_date.month - self.start_date.month
            )

            if self.end_date.day > self.start_date.day:
                months += 1

            months = max(1, months)

            self.total_price = self.office.price_per_month * months

        super().save(*args, **kwargs)

    def __str__(self):
        item = self.meeting_room or self.office
        return f"{self.client_name} - {item}"
    
# events
class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    event_date = models.DateField()
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.title
    
# gallery
class GalleryImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# FAQ
class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
# contact
class Contact(models.Model):
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.phone
    
# visit requests
class VisitRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
# business registrations
class BusinessRegistration(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Government Approval"),
        ("active", "Active CR"),
        ("rejected", "Application Rejected"),
    ]
    
    REQUEST_TYPE = [('new', 'New Registration'), ('renewal', 'CR Renewal')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_requests")
    company_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    commercial_registration = models.CharField(max_length=100, blank=True, help_text="Required for renewals.")
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE, default='new')
    business_type = models.CharField(max_length=100)
    cpr_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Required Documents
    cpr_document = models.FileField(upload_to='business_docs/cpr/', blank=True, null=True, help_text="Upload copy of CPR.")
    passport_document = models.FileField(upload_to='business_docs/passport/', blank=True, null=True, help_text="Upload copy of Passport.")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} ({self.get_request_type_display()})"

# referrals
class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    referred_company = models.CharField(max_length=150)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name