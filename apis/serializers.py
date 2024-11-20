from rest_framework import serializers
from .models import * 

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication 
        # fields = ['name', 'description', 'dosage_measurement', 'instructions'] 
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription 
        fields = '__all__'

class MedicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDetail
        fields = '__all__'
