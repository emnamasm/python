from django.contrib import admin

# Register your models here.
from .models import Participant,Reservation
admin.site.register(Participant)
admin.site.register(Reservation)
