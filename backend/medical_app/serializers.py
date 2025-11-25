from rest_framework import serializers
from .models import PatientData

class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientData
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'prediction_made')


class PredictionRequestSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=1, max_value=120)
    gender = serializers.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    
    # Lab Results
    glucose = serializers.FloatField(min_value=0.0, max_value=30.0)
    cholesterol = serializers.FloatField(min_value=0.0, max_value=15.0)
    triglycerides = serializers.FloatField(min_value=0.0, max_value=10.0)
    creatinine = serializers.FloatField(min_value=0.0, max_value=1000.0)
    uree = serializers.FloatField(min_value=0.0, max_value=50.0)
    uric_acid = serializers.FloatField(min_value=0.0, max_value=1000.0)
    got = serializers.FloatField(min_value=0.0, max_value=500.0)
    gpt = serializers.FloatField(min_value=0.0, max_value=500.0)
    bilirubin = serializers.FloatField(min_value=0.0, max_value=100.0)
    
    smoking = serializers.BooleanField(default=False)
    obesity = serializers.BooleanField(default=False)
    family_history = serializers.BooleanField(default=False)


class PredictionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    diagnosis = serializers.CharField()
    probabilities = serializers.DictField()
    created_at = serializers.DateTimeField()
