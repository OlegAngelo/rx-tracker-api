from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import *
from .serializers import *

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # need token to access api
def get_medications(request):
    medications_object = Medication.objects.all()
    medication_list = MedicationSerializer(medications_object, many=True)

    return Response(medication_list.data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # need token to access api
def add_medication(request):
  serializer = MedicationSerializer(data=request.data)

  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
