from django.db import models
from datetime import timedelta  # Used to compute the end_date

# Patient model: Represents the patient entity in the database.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated unique ID for each patient
    name = models.CharField(max_length=255, null=True, blank=True)  # Optional name field with a max length of 255 characters

    def __str__(self):
        # String representation of the Patient model, helpful in Django Admin or shell
        return f"Patient {self.id} - {self.name if self.name else 'No Name'}"

# Medication model: Represents standardized medications if reused across prescriptions.
class Medication(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated unique ID for each medication
    name = models.CharField(max_length=255)  # Name of the medication
    description = models.TextField(null=True, blank=True)  # Optional detailed description of the medication
    dosage_measurement = models.CharField(max_length=50)  # Dosage amount, e.g., "500mg"
    instructions = models.TextField(null=True, blank=True)  # Optional instructions, e.g., "Take with food"

    def __str__(self):
        # String representation of the Medication model
        return self.name

# Prescription model: Represents a prescription for a patient.
class Prescription(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generated unique ID for each prescription
    patient = models.ForeignKey(
        Patient,  # Links to the Patient model
        on_delete=models.CASCADE,  # Deletes prescriptions if the associated patient is deleted
        related_name="prescriptions"  # Allows reverse lookup, e.g., patient.prescriptions.all()
    )
    start_date = models.DateField()  # The date the prescription starts
    duration = models.PositiveIntegerField()  # Duration of the prescription in days
    end_date = models.DateField()  # The computed end date of the prescription
    completed_date = models.DateField(null=True, blank=True)  # Optional date when the prescription was completed
    is_completed = models.BooleanField(default=False)  # Tracks whether the prescription is completed

    # Overriding the save method to compute the end_date dynamically
    def save(self, *args, **kwargs):
        if self.start_date and self.duration:
            # Compute end_date as start_date + duration
            self.end_date = self.start_date + timedelta(days=self.duration)
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        # String representation of the Prescription model
        return f"Prescription {self.id} for Patient {self.patient.id}"

# MedicationDetails model: Represents details of medications in a specific prescription.
class MedicationDetail(models.Model):
    prescription = models.ForeignKey(
        Prescription,  # Links to the Prescription model
        on_delete=models.CASCADE,  # Deletes medication details if the associated prescription is deleted
        related_name="medication_detail"  # Allows reverse lookup, e.g., prescription.medication_details.all()
    )
    medication = models.ForeignKey(
        Medication,  # Links to the Medication model for reuse
        on_delete=models.CASCADE  # Deletes medication details if the associated medication is deleted
    )
    dosage = models.CharField(max_length=50)  # Dosage for this medication in this prescription, e.g., "1 tablet"
    frequency = models.CharField(max_length=50)  # Frequency of intake, e.g., "Twice a day"
    intake_date = models.DateField(null=True, blank=True)  # Optional specific intake date
    intake_time = models.TimeField(null=True, blank=True)  # Optional specific intake time

    def __str__(self):
        # String representation of the MedicationDetails model
        return f"{self.medication.name} - Prescription {self.prescription.id}"
