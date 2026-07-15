from django.contrib import admin
from .models import (Service, Feature, Branch, MeetingRoom, Event, GalleryImage, FAQ, Contact, VisitRequest, BusinessRegistration, Referral, Office, Booking)

# Register your models here.
admin.site.register(Service)
admin.site.register(Feature)
admin.site.register(Branch)
admin.site.register(MeetingRoom)
admin.site.register(Event)
admin.site.register(GalleryImage)
admin.site.register(FAQ)
admin.site.register(Contact)
admin.site.register(VisitRequest)
admin.site.register(BusinessRegistration)
admin.site.register(Referral)
admin.site.register(Office)
admin.site.register(Booking)
