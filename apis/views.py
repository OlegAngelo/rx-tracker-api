from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# from collections import defaultdict
from datetime import date, timedelta
from django.db import transaction, IntegrityError

from .serializers import *


# Prescriptions API

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_prescriptions(request):
    user = request.user
    prescriptions = Prescription.objects.filter(user=user.id)

    # Prepare a list to store the response data
    response_data = []

    for prescription in prescriptions:
        # Calculate the intake dates based on start_date and duration
        start_date = prescription.start_date
        end_date = start_date + timedelta(days=prescription.duration - 1)

        # Iterate over each day within the duration and add medication details
        for day_offset in range(prescription.duration):
            intake_date = start_date + timedelta(days=day_offset)
            medication_details = MedicationDetail.objects.filter(
                prescription=prescription,
                intake_date=intake_date
            )

            if medication_details.exists():
                serialized_medication_details = []
                for detail in medication_details:
                    serialized_detail = {
                        "medication_name": detail.medication_name,
                        "frequency": detail.frequency,
                        "dosage_measurement": detail.dosage_measurement,
                        "prescription": detail.prescription.id,
                        "instructions": detail.instructions,
                    }
                    serialized_medication_details.append(serialized_detail)

                # Add the day's data to the response list
                response_data.append({
                    "intake_date": intake_date.strftime("%Y-%m-%d"),
                    "medication_details": serialized_medication_details
                })

    if not response_data:
        return Response({"message": f"No prescriptions found for {user.first_name} {user.last_name}."}, status=status.HTTP_404_NOT_FOUND)

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_prescription(request):
    request_data = request.data.copy()
    request_data['user'] = request.user.id  # Add the logged-in user to the request data

    try:
        with transaction.atomic():
            # Check if medication details exist in the request
            medication_details_data = request_data.get('medication_details')
            if not medication_details_data:
                return Response({"error": "No medication details provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the serializer instance and validate the prescription data
            prescription_serializer = PrescriptionSerializer(data=request_data)
            if not prescription_serializer.is_valid():
                return Response(prescription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the main prescription instance
            prescription_serializer.save()

            return Response(prescription_serializer.data, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        # Handle specific database integrity errors
        transaction.rollback()  # Explicit rollback for clarity, though transaction.atomic() does this automatically
        print(f"Database integrity error: {e}")
        return Response({"error": "Database integrity error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # Handle any other unexpected errors
        transaction.rollback()  # Explicit rollback for clarity, though transaction.atomic() does this automatically
        print(f"An error occurred: {e}")
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_prescription(request, pk):
    try:
        prescription = Prescription.objects.get(id=pk, user=request.user.id)
    except Prescription.DoesNotExist:
        return Response(
            {"detail": "Prescription not found or not owned by the user."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_prescription(request, pk):
    try:
        prescription = Prescription.objects.get(id=pk, user=request.user.id)
        prescription.delete()
        return Response({"detail": "Prescription deleted."}, status=status.HTTP_204_NO_CONTENT)
    except Prescription.DoesNotExist:
        return Response(
            {"detail": "Prescription not found or not owned by the user."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complete_prescription(request, prescription_id):
    try:
        prescription = Prescription.objects.get(id=prescription_id)

        if prescription.is_completed:
            return Response(
                {"detail": "Prescription is already marked as completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        prescription.is_completed = True
        prescription.completed_date = date.today()
        prescription.save()

        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Prescription.DoesNotExist:
        return Response(
            {"detail": "Prescription not found."},
            status=status.HTTP_404_NOT_FOUND
        )

# Medications API

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_medications_by_date(request):
#     user = request.user.id
#     prescriptions = Prescription.objects.filter(user=user)
#
#     if not prescriptions.exists():
#         return Response({'detail': 'No medications found.'}, status=status.HTTP_204_NO_CONTENT)
#
#     medication_details = MedicationDetail.objects.filter(prescription__in=prescriptions)
#
#     if not medication_details.exists():
#         return Response({'detail': 'No medications found.'}, status=status.HTTP_204_NO_CONTENT)
#
#     grouped_medications = defaultdict(list)
#     for medication in medication_details:
#         grouped_medications[medication.intake_date].append(medication)
#
#     response_data = [
#         {'date': intake_date, 'medications': MedicationDetailSerializer(medications, many=True).data}
#         for intake_date, medications in grouped_medications.items()
#     ]
#
#     return Response(response_data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_medication(request):
#     serializer = MedicationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
