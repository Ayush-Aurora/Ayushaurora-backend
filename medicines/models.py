from django.db import models

# Create your models here.
class RawMedicineData(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_1mg = models.BigIntegerField(db_column='ID_1MG', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    manufacturer_name = models.CharField(max_length=1000, blank=True, null=True)
    pack_size_label = models.CharField(max_length=500, blank=True, null=True)
    quantity = models.SmallIntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    is_discontinued = models.IntegerField(blank=True, null=True)
    prescription_required = models.IntegerField(blank=True, null=True)
    composition = models.CharField(max_length=1000, blank=True, null=True)
    mrp_india = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'raw_medicine_data'