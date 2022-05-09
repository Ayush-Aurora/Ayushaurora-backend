from rest_framework import serializers
from .models import RawMedicineData

class RawMedicineDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMedicineData
        fields = ['id', 'name', 'type', 'quantity' , 'pack_size_label']