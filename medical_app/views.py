from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import PatientForm
from .models import PatientData
from .ml_model import MedicalDiagnosisModel

ml_model = MedicalDiagnosisModel()

def index(request):
    return render(request, 'medical_app/index.html')

def train_model(request):
    if request.method == 'POST':
        accuracy = ml_model.train_model()
        tree_image = ml_model.visualize_tree()
        feature_importance = ml_model.get_feature_importance()
        
        context = {
            'accuracy': round(accuracy * 100, 2),
            'tree_image': tree_image,
            'feature_importance': feature_importance.to_dict('records') if feature_importance is not None else [],
        }
        return render(request, 'medical_app/dataset.html', context)
    
    return render(request, 'medical_app/dataset.html')

def predict_diagnosis(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            
            patient_data = {
                'age': patient.age,
                'gender': patient.gender,
                'fever': 1 if patient.fever else 0,
                'cough': 1 if patient.cough else 0,
                'chest_pain': 1 if patient.chest_pain else 0,
                'shortness_breath': 1 if patient.shortness_breath else 0,
                'fatigue': 1 if patient.fatigue else 0,
                'headache': 1 if patient.headache else 0,
                'nausea': 1 if patient.nausea else 0,
                'blood_pressure': patient.blood_pressure,
                'cholesterol': patient.cholesterol,
                'blood_sugar': patient.blood_sugar,
                'smoking': 1 if patient.smoking else 0,
                'obesity': 1 if patient.obesity else 0,
                'family_history': 1 if patient.family_history else 0,
            }
            
            diagnosis, probabilities = ml_model.predict(patient_data)
            
            if diagnosis:
                patient.diagnosis = diagnosis
                patient.prediction_made = True
                patient.save()
                
                # Redirect to results page - POST-Redirect-GET pattern
                return redirect('show_results', patient_id=patient.id)
            else:
                form.add_error(None, "Erreur lors de la prédiction.")
    else:
        form = PatientForm()
    
    return render(request, 'medical_app/predict.html', {'form': form})

def show_results(request, patient_id):
    """Display prediction results for a specific patient"""
    try:
        patient = PatientData.objects.get(id=patient_id)
        
        diagnosis_map = {
            'SAIN': 'Patient Sain',
            'DIABETE': 'Diabète',
            'HYPER': 'Hypertension',
            'CARDIAC': 'Problème Cardiaque',
            'RESPIRATORY': 'Problème Respiratoire',
        }
        
        # Recreate patient data for getting fresh diagnosis and probabilities
        patient_data = {
            'age': patient.age,
            'gender': patient.gender,
            'fever': 1 if patient.fever else 0,
            'cough': 1 if patient.cough else 0,
            'chest_pain': 1 if patient.chest_pain else 0,
            'shortness_breath': 1 if patient.shortness_breath else 0,
            'fatigue': 1 if patient.fatigue else 0,
            'headache': 1 if patient.headache else 0,
            'nausea': 1 if patient.nausea else 0,
            'blood_pressure': patient.blood_pressure,
            'cholesterol': patient.cholesterol,
            'blood_sugar': patient.blood_sugar,
            'smoking': 1 if patient.smoking else 0,
            'obesity': 1 if patient.obesity else 0,
            'family_history': 1 if patient.family_history else 0,
        }
        
        # Get fresh diagnosis and probabilities
        diagnosis, probabilities = ml_model.predict(patient_data)
        
        context = {
            'patient': patient,
            'diagnosis': diagnosis_map.get(diagnosis, diagnosis),  # Use fresh diagnosis, not stored one
            'probabilities': probabilities,
        }
        return render(request, 'medical_app/results.html', context)
    except PatientData.DoesNotExist:
        return redirect('predict_diagnosis')

def model_info(request):
    ml_model.load_model()
    tree_image = ml_model.visualize_tree()
    feature_importance = ml_model.get_feature_importance()
    
    context = {
        'tree_image': tree_image,
        'feature_importance': feature_importance.to_dict('records') if feature_importance is not None else [],
    }
    return render(request, 'medical_app/model_info.html', context)

@csrf_exempt
def api_predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            patient_data = {
                'age': int(data['age']),
                'gender': data['gender'],
                'fever': bool(data.get('fever', False)),
                'cough': bool(data.get('cough', False)),
                'chest_pain': bool(data.get('chest_pain', False)),
                'shortness_breath': bool(data.get('shortness_breath', False)),
                'fatigue': bool(data.get('fatigue', False)),
                'headache': bool(data.get('headache', False)),
                'nausea': bool(data.get('nausea', False)),
                'blood_pressure': int(data['blood_pressure']),
                'cholesterol': int(data['cholesterol']),
                'blood_sugar': int(data['blood_sugar']),
                'smoking': bool(data.get('smoking', False)),
                'obesity': bool(data.get('obesity', False)),
                'family_history': bool(data.get('family_history', False)),
            }
            
            diagnosis, probabilities = ml_model.predict(patient_data)
            
            if diagnosis:
                diagnosis_map = {
                    'SAIN': 'Patient Sain',
                    'DIABETE': 'Diabète',
                    'HYPER': 'Hypertension',
                    'CARDIAC': 'Problème Cardiaque',
                    'RESPIRATORY': 'Problème Respiratoire',
                }
                
                return JsonResponse({
                    'diagnosis': diagnosis_map.get(diagnosis, diagnosis),
                    'probabilities': probabilities,
                    'success': True
                })
            else:
                return JsonResponse({'error': 'Erreur de prédiction'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)