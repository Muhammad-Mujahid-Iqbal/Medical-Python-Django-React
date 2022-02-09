"""Goal serializers file."""
from rest_framework import serializers
from patient.models import Patient,Visit


class VisitSerializer(serializers.ModelSerializer):
    """Serializer class for model Visit


    Parameters
    ----------
    serializers : rest_framework

    """

    class Meta:
        """Meta class for Serializer GoalSerializer"""

        model = Visit
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    """Serializer class for model Patient


    Parameters
    ----------
    serializers : rest_framework

    """

    class Meta:
        """Meta class for Serializer GoalSerializer"""

        model = Patient
        fields = "__all__"
    
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['visits']=VisitSerializer(instance.p_visits.all(),many=True).data
        return response
        