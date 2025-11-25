from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PatientData
from .serializers import PredictionRequestSerializer, PredictionResponseSerializer, PatientDataSerializer
from .ml_model import MedicalDiagnosisModel

ml_model = MedicalDiagnosisModel()


@api_view(['POST'])
def train_model_api(request):
    """Train the ML model"""
    try:
        accuracy = ml_model.train_model()
        return Response({
            'success': True,
            'accuracy': round(accuracy * 100, 2),
            'message': 'Model trained successfully'
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def predict_api(request):
    """Make a prediction"""
    serializer = PredictionRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        patient_data = serializer.validated_data
        
        # Prepare data for ML model
        ml_data = {
            'age': patient_data['age'],
            'gender': patient_data['gender'],
            'glucose': patient_data['glucose'],
            'cholesterol': patient_data['cholesterol'],
            'triglycerides': patient_data['triglycerides'],
            'creatinine': patient_data['creatinine'],
            'uree': patient_data['uree'],
            'uric_acid': patient_data['uric_acid'],
            'got': patient_data['got'],
            'gpt': patient_data['gpt'],
            'bilirubin': patient_data['bilirubin'],
            'smoking': 1 if patient_data['smoking'] else 0,
            'obesity': 1 if patient_data['obesity'] else 0,
            'family_history': 1 if patient_data['family_history'] else 0,
        }
        
        # Make prediction
        diagnosis, probabilities = ml_model.predict(ml_data)
        
        if not diagnosis:
            return Response({
                'error': 'Model not trained or prediction failed'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save to database
        patient = PatientData.objects.create(
            age=patient_data['age'],
            gender=patient_data['gender'],
            glucose=patient_data['glucose'],
            cholesterol=patient_data['cholesterol'],
            triglycerides=patient_data['triglycerides'],
            creatinine=patient_data['creatinine'],
            uree=patient_data['uree'],
            uric_acid=patient_data['uric_acid'],
            got=patient_data['got'],
            gpt=patient_data['gpt'],
            bilirubin=patient_data['bilirubin'],
            smoking=patient_data['smoking'],
            obesity=patient_data['obesity'],
            family_history=patient_data['family_history'],
            diagnosis=diagnosis,
            prediction_made=True
        )
        
        # Return response
        return Response({
            'id': patient.id,
            'diagnosis': diagnosis,
            'probabilities': probabilities,
            'created_at': patient.created_at
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def history_api(request):
    """Get prediction history"""
    try:
        patients = PatientData.objects.filter(prediction_made=True).order_by('-created_at')
        serializer = PatientDataSerializer(patients, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def result_detail_api(request, patient_id):
    """Get specific result"""
    try:
        patient = PatientData.objects.get(id=patient_id, prediction_made=True)
        serializer = PatientDataSerializer(patient)
        return Response(serializer.data)
    except PatientData.DoesNotExist:
        return Response({
            'error': 'Patient not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'Medical Diagnosis API',
        'version': '2.0'
    })


from django.http import FileResponse
from .utils import generate_pdf

@api_view(['GET'])
def download_prescription_pdf(request, patient_id):
    """Generate and download prescription PDF"""
    try:
        patient = PatientData.objects.get(id=patient_id, prediction_made=True)
        buffer = generate_pdf(patient)
        
        filename = f"Ordonnance_Patient_{patient_id}_{patient.created_at.strftime('%Y-%m-%d')}.pdf"
        
        return FileResponse(
            buffer, 
            as_attachment=True, 
            filename=filename,
            content_type='application/pdf'
        )
    except PatientData.DoesNotExist:
        return Response({
            'error': 'Patient not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
