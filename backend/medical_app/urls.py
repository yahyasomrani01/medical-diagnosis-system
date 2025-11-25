from django.urls import path
from . import api_views
from . import api_views

urlpatterns = [
    #API endpoints
    path('api/health/', api_views.health_check, name='api_health'),
    path('api/train/', api_views.train_model_api, name='api_train'),
    path('api/predict/', api_views.predict_api, name='api_predict'),
    path('api/history/', api_views.history_api, name='history_api'),
    path('api/results/<int:patient_id>/', api_views.result_detail_api, name='result_detail_api'),
    path('api/prescription/<int:patient_id>/', api_views.download_prescription_pdf, name='download_prescription_pdf'),
]