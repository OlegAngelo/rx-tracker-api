from rest_framework import serializers
from .models import *

class MedicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDetail
        fields = [
            'id',
            'medication_name',
            'dosage_measurement',
            'frequency',
            'instructions',
            'intake_time',
            'intake_date',
            'is_completed'
        ]
        read_only_fields = ['intake_date']

class PrescriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    medication_details = MedicationDetailSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'user',
            'start_date',
            'duration',
            'end_date',
            'completed_date',
            'is_completed',
            'medication_details',
        ]
        read_only_fields = ['end_date', 'completed_date']

    def create(self, validated_data):
        medication_details_data = validated_data.pop('medication_details', [])
        prescription = Prescription.objects.create(**validated_data)
        prescription.create_medical_details(medication_details_data)

        # duration = validated_data.get('duration', 0)
        # for detail_data in medication_details_data:
        #     for intake_day in range(duration):
        #         intake_date = validated_data['start_date'] + timedelta(days=intake_day)
        #         MedicationDetail.objects.create(
        #             prescription=prescription,
        #             intake_date=intake_date,
        #             **detail_data
        #         )

        return prescription

    def update(self, instance, validated_data):
        medication_details_data = validated_data.pop('medication_details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if medication_details_data:
            instance.medication_details.all().delete()
            for detail_data in medication_details_data:
                MedicationDetail.objects.create(prescription=instance, **detail_data)

        return instance
