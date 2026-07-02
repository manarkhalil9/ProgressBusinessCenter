from django.db import models

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
