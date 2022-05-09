from django.shortcuts import render
from rest_framework import generics,status,viewsets
from .serializers import PrescriptionCreateSerializer
from .models import Prescriptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class CreatePrescriptionView(generics.GenericAPIView):
    serializer_class = PrescriptionCreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self , request):
        # print(request)
        user = request.user
        if user.role != 2:
            return Response({'error': 'Only Doctors are allowed to create prescription!'} , status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data=request.data)
        validated_data,medicines = serializer.validate(data=request.data)
        prescription = serializer.create(validated_data=validated_data , medicines=medicines)
        return Response({'status': 'Prescription created successfully!' , 'id': prescription.id , 'pid': prescription.pid} , status = status.HTTP_200_OK)

class FetchPrescriptionView(generics.GenericAPIView):
    serializer_class = PrescriptionCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self , request):
        user = request.user
        if user.role != 2:
            return Response({'error': 'Only Doctors are allowed to fetch prescription!'} , status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(data=request.data)
        # prescription = Prescriptions.objects.using('doctors_db').all()
        prescription = serializer.fetch_by_id(data=request.data)
        return Response({'id': prescription.id, 
                         'pid': prescription.pid, 
                         'patient': prescription.patient_id,
                         'doctor': prescription.doctor_id
                        } , status=status.HTTP_200_OK)