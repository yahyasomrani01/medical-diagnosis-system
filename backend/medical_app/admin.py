from django.contrib import admin
from .models import PatientData

@admin.register(PatientData)
class PatientDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'age', 'gender', 'diagnosis', 'created_at']
    list_filter = ['gender', 'diagnosis', 'created_at']
    search_fields = ['diagnosis']