from django.contrib import admin
from .models import RawMedicineData

# Register your models here.
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'quantity' , 'pack_size_label']

admin.site.register(RawMedicineData, MedicineAdmin)