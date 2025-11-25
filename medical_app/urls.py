from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('train/', views.train_model, name='train_model'),
    path('predict/', views.predict_diagnosis, name='predict_diagnosis'),
    path('results/<int:patient_id>/', views.show_results, name='show_results'),
    path('model-info/', views.model_info, name='model_info'),
    path('api/predict/', views.api_predict, name='api_predict'),
]