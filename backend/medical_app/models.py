from django.db import models

class PatientData(models.Model):
    age = models.IntegerField()
    GENDER_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    # Lab Results
    glucose = models.FloatField(help_text="Glucose (mmol/L)")
    cholesterol = models.FloatField(help_text="Cholesterol (mmol/L)")
    triglycerides = models.FloatField(help_text="Triglycerides (mmol/L)")
    creatinine = models.FloatField(help_text="Creatinine (umol/L)")
    uree = models.FloatField(help_text="Uree (mmol/L)")
    uric_acid = models.FloatField(help_text="Uric Acid (umol/L)")
    got = models.FloatField(help_text="GOT (U/L)")
    gpt = models.FloatField(help_text="GPT (U/L)")
    bilirubin = models.FloatField(help_text="Bilirubin Total (umol/L)")
    
    # Risk Factors
    smoking = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)
    family_history = models.BooleanField(default=False)
    
    DIAGNOSIS_CHOICES = [
        ('SAIN', 'Patient Sain'),
        ('DIABETE', 'Diabète'),
        ('HYPERLIPIDEMIE', 'Hyperlipidémie'),
        ('RENAL', 'Insuffisance Rénale'),
        ('HEPATIQUE', 'Insuffisance Hépatique'),
    ]
    diagnosis = models.CharField(max_length=20, choices=DIAGNOSIS_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    prediction_made = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient {self.id} - {self.get_diagnosis_display()}"