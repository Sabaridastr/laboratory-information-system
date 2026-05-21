from rest_framework import serializers
from .models import Patient, Test


# 🔹 Patient Serializer
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


# 🔹 Test Serializer
class TestSerializer(serializers.ModelSerializer):
    # Show patient name (extra readable field)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Test
        fields = '__all__'