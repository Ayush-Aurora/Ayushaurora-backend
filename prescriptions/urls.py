from django.urls import path
from .views import CreatePrescriptionView,FetchPrescriptionView

urlpatterns = [
    path('create_prescription/', CreatePrescriptionView.as_view(), name="create_prescription"),
    path('prescription/' , FetchPrescriptionView.as_view() , name='fetch-prescription')
]