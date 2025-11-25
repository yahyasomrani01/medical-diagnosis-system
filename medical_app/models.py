from django.db import models

class PatientData(models.Model):
    age = models.IntegerField()
    GENDER_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    fever = models.BooleanField(default=False)
    cough = models.BooleanField(default=False)
    chest_pain = models.BooleanField(default=False)
    shortness_breath = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    nausea = models.BooleanField(default=False)
    
    blood_pressure = models.IntegerField()
    cholesterol = models.IntegerField()
    blood_sugar = models.IntegerField()
    
    smoking = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)
    family_history = models.BooleanField(default=False)
    
    DIAGNOSIS_CHOICES = [
        ('SAIN', 'Patient Sain'),
        ('DIABETE', 'Diabète'),
        ('HYPER', 'Hypertension'),
        ('CARDIAC', 'Problème Cardiaque'),
        ('RESPIRATORY', 'Problème Respiratoire'),
    ]
    diagnosis = models.CharField(max_length=20, choices=DIAGNOSIS_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prediction_made = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient {self.id} - {self.get_diagnosis_display()}"