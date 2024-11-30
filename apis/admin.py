from django.contrib import admin

# Register your models here.
from .models import Prescription, MedicationDetail

myModels = [Prescription, MedicationDetail]  # iterable list
admin.site.register(myModels)
