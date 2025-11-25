import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to prevent macOS crash
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import joblib
import os
from django.conf import settings

class MedicalDiagnosisModel:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_names = []
        self.class_names = ['SAIN', 'DIABETE', 'HYPER', 'CARDIAC', 'RESPIRATORY']
        
    def generate_sample_data(self):
        np.random.seed(42)
        n_samples = 200
        
        data = {
            'age': np.random.randint(18, 80, n_samples),
            'gender': np.random.choice(['M', 'F'], n_samples),
            'fever': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'cough': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'chest_pain': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'shortness_breath': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'fatigue': np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
            'headache': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'nausea': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'blood_pressure': np.random.randint(90, 180, n_samples),
            'cholesterol': np.random.randint(150, 300, n_samples),
            'blood_sugar': np.random.randint(70, 200, n_samples),
            'smoking': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'obesity': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'family_history': np.random.choice([0, 1], n_samples, p=[0.5, 0.5]),
        }
        
        df = pd.DataFrame(data)
        
        diagnoses = []
        for idx, row in df.iterrows():
            if row['blood_sugar'] > 126 and row['age'] > 45:
                diagnoses.append('DIABETE')
            elif row['blood_pressure'] > 140 and row['age'] > 50:
                diagnoses.append('HYPER')
            elif row['chest_pain'] and row['shortness_breath'] and row['cholesterol'] > 240:
                diagnoses.append('CARDIAC')
            elif row['cough'] and row['shortness_breath'] and row['fever']:
                diagnoses.append('RESPIRATORY')
            else:
                diagnoses.append('SAIN')
                
        df['diagnosis'] = diagnoses
        return df
    
    def preprocess_data(self, df):
        df_encoded = df.copy()
        categorical_columns = ['gender', 'diagnosis']
        for col in categorical_columns:
            self.label_encoders[col] = LabelEncoder()
            df_encoded[col] = self.label_encoders[col].fit_transform(df[col])
        
        self.feature_names = [col for col in df.columns if col != 'diagnosis']
        return df_encoded
    
    def train_model(self):
        df = self.generate_sample_data()
        df_processed = self.preprocess_data(df)
        
        X = df_processed[self.feature_names]
        y = df_processed['diagnosis']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model = DecisionTreeClassifier(
            criterion='entropy',
            max_depth=5,
            min_samples_split=10,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        model_path = os.path.join(settings.BASE_DIR, 'medical_model.joblib')
        joblib.dump({
            'model': self.model,
            'encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'class_names': self.class_names
        }, model_path)
        
        return accuracy
    
    def load_model(self):
        try:
            model_path = os.path.join(settings.BASE_DIR, 'medical_model.joblib')
            saved_data = joblib.load(model_path)
            self.model = saved_data['model']
            self.label_encoders = saved_data['encoders']
            self.feature_names = saved_data['feature_names']
            self.class_names = saved_data['class_names']
            return True
        except:
            return False
    
    def predict(self, patient_data):
        if not self.model:
            if not self.load_model():
                return None, None
        
        input_data = pd.DataFrame([patient_data])
        
        for col in input_data.columns:
            if col in self.label_encoders:
                try:
                    input_data[col] = self.label_encoders[col].transform(input_data[col])
                except ValueError:
                    input_data[col] = 0
        
        input_data = input_data[self.feature_names]
        prediction = self.model.predict(input_data)[0]
        probabilities = self.model.predict_proba(input_data)[0]
        
        diagnosis = self.label_encoders['diagnosis'].inverse_transform([prediction])[0]
        prob_dict = {
            self.class_names[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        return diagnosis, prob_dict
    
    def visualize_tree(self):
        if not self.model:
            return None
            
        plt.figure(figsize=(15, 10))
        plot_tree(self.model,
                 feature_names=self.feature_names,
                 class_names=self.class_names,
                 filled=True,
                 rounded=True,
                 fontsize=8)
        
        plt.title("Arbre de Décision - Diagnostic Médical")
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close()
        
        return graphic
    
    def get_feature_importance(self):
        if not self.model:
            return None
            
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df