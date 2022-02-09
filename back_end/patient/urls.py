
from django.urls import path

from patient.views import PatientView

urlpatterns = [
    path("patients/", PatientView.as_view()),\
]
