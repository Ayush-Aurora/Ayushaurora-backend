from rest_framework import serializers
from .models import Prescriptions
from medicines.models import RawMedicineData
from ayushauth.models import User

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriptions
        fields = ['patient', 'doctor', 'medicines', 'created_at']
    
    def validate(self, data):
        patientdata = User.objects.filter(id=data['patient']).get()
        doctordata = User.objects.filter(id=data['doctor']).get()
        if(patientdata.role != 3 and doctordata.role != 2):
            raise serializers.ValidationError("Invalid patient or doctor id provided")
        validated_data = {
            'patient': patientdata,
            'doctor': doctordata,
        }
        medicines = []
        for medicine in data['medicines']:
            medicine_data = RawMedicineData.objects.using('doctors_db').filter(id=medicine).get()
            medicines.append(medicine_data)
        return validated_data,medicines

    def create(self , validated_data , medicines):
        print(validated_data)
        prescription = Prescriptions.objects.using('doctors_db').create(**validated_data)
        prescription.medicines.set(medicines)

        # for medicine in validated_data['medicines']:
        #     prescription.medicines.append(medicine)
        prescription.save()

        return prescription

    def fetch_by_id(self , data):
        fetched_prescription = Prescriptions.objects.using('doctors_db').filter(id = data['id']).get()
        return fetched_prescription