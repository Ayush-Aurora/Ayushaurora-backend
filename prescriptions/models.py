from django.db import models
from ayushauth.models import User
from django.utils import timezone
import uuid
from medicines.models import RawMedicineData
# Create your models here.

class Prescriptions(models.Model):
    pid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Identifier')
    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='patientid' , db_constraint=False)
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctorid' , db_constraint=False)
    medicines = models.ManyToManyField(RawMedicineData , db_constraint=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
        db_table = 'prescriptions'

    def _str_(self):
        return f'{self.patientid} by {self.doctorid} - {self.medid} on {self.created}'