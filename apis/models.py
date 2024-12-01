from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

# Prescription model (One prescription per user)
class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    start_date = models.DateField()
    duration = models.PositiveIntegerField()
    # auto-generated fields
    end_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False) # true when all is completed under this prescription

    # Automatically compute the end date if start_date and duration are provided
    def save(self, *args, **kwargs):
        if self.start_date and self.duration:
            self.end_date = self.start_date + timedelta(days=self.duration)
        super().save(*args, **kwargs)

    # create multiple medical details based on number of duration
    def create_medical_details(self, medical_details_data):
        for med_detail in medical_details_data:
            for day in range(self.duration):
                intake_date = self.start_date + timedelta(days=day)
                MedicationDetail.objects.create(
                    prescription=self,
                    intake_date=intake_date,
                    **med_detail
                )

    def __str__(self):
        return f"Prescription {self.id} for user {self.user.username}"


# MedicationDetails model (Links prescriptions to medications with additional details)
class MedicationDetail(models.Model):
    id = models.AutoField(primary_key=True),
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="medication_details"
    )
    medication_name = models.CharField(max_length=200)
    dosage_measurement = models.CharField(max_length=50)
    frequency = models.PositiveIntegerField()
    instructions = models.TextField(null=True, blank=True)
    intake_time = models.TimeField(null=True, blank=True) # time to take the med
    # auto-generated fields
    intake_date = models.DateField(null=True, blank=True) # generated based on start date to end date (1 data per date)
    is_completed = models.BooleanField(default=False) # generated when item is complete

    def __str__(self):
        return f"{self.medication_name} - Prescription {self.prescription.id}"
