from django.contrib import admin

# Register your models here.
from .models import Medication, Prescription, Patient, MedicationDetail

myModels = [Medication, Prescription, Patient, MedicationDetail]  # iterable list
admin.site.register(myModels)
