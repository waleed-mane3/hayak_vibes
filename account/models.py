from django.db import models
from auth_system.models import CustomUser
import uuid
from django.utils import timezone



class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500, blank=True, null=True, default="none")
    venue = models.CharField(max_length=500, blank=True, null=True, default="none")
    groom = models.CharField(max_length=500, blank=True, null=True, default="none")
    bride = models.CharField(max_length=500, blank=True, null=True, default="none")
    date = models.DateTimeField(default=timezone.now)
    capacity = models.IntegerField(null=True, blank=True)

    
    def __str__(self):
        return self.name



class Invitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('waiting', 'waiting'),
        ('confirmed', 'confirmed'),
        ('apologized', 'apologized'),
        ('checked', 'checked')
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=500, null=False, blank=False)
    mobile = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=300, choices = STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=36, default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name
