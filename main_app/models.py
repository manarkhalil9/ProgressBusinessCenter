from django.db import models
from django.contrib.auth.models import User

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
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# meeting rooms
class MeetingRoom(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='meeting_rooms')
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
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
    image_url = models.URLField()
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
    address = models.TextField()
    google_map = models.URLField(blank=True)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business")
    company_name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=100)
    commercial_registration = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    services = models.ManyToManyField(Service, blank=True, related_name='businesses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

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