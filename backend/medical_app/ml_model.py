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
        self.class_names = ['SAIN', 'DIABETE', 'HYPERLIPIDEMIE', 'RENAL', 'HEPATIQUE']
        
    def generate_sample_data(self):
        np.random.seed(42)
        n_samples = 1000
        
        # Generate realistic lab data
        data = {
            'age': np.random.randint(18, 90, n_samples),
            'gender': np.random.choice(['M', 'F'], n_samples),
            
            # Metabolic
            'glucose': np.random.normal(5.0, 1.5, n_samples),  # Normal 3.9-6.4
            'cholesterol': np.random.normal(4.5, 1.0, n_samples), # Normal 3.6-6.0
            'triglycerides': np.random.normal(1.2, 0.5, n_samples), # Normal 0.0-1.9
            
            # Kidney
            'creatinine': np.random.normal(80, 20, n_samples), # Normal 50-120
            'uree': np.random.normal(5.0, 1.5, n_samples), # Normal 3.5-8.5
            'uric_acid': np.random.normal(300, 80, n_samples), # Normal 208-428
            
            # Liver
            'got': np.random.normal(25, 10, n_samples), # Normal 0-40
            'gpt': np.random.normal(25, 10, n_samples), # Normal 0-40
            'bilirubin': np.random.normal(10, 5, n_samples), # Normal 2.0-21.0
        }
        
        # Ensure no negative values
        for key in data:
            if key != 'gender':
                data[key] = np.abs(data[key])
        
        df = pd.DataFrame(data)
        
        diagnoses = []
        for idx, row in df.iterrows():
            # Diagnosis Rules
            if row['glucose'] > 7.0:
                diagnoses.append('DIABETE')
            elif row['cholesterol'] > 6.2 or row['triglycerides'] > 2.3:
                diagnoses.append('HYPERLIPIDEMIE')
            elif row['creatinine'] > 130 or row['uree'] > 9.0:
                diagnoses.append('RENAL')
            elif row['got'] > 50 or row['gpt'] > 50 or row['bilirubin'] > 25:
                diagnoses.append('HEPATIQUE')
            else:
                diagnoses.append('SAIN')
                
        df['diagnosis'] = diagnoses
        return df
    
    def preprocess_data(self, df):
        df_encoded = df.copy()
        # Encode gender
        le_gender = LabelEncoder()
        df_encoded['gender'] = le_gender.fit_transform(df['gender'])
        self.label_encoders['gender'] = le_gender
        
        # Encode diagnosis
        le_diagnosis = LabelEncoder()
        df_encoded['diagnosis'] = le_diagnosis.fit_transform(df['diagnosis'])
        self.label_encoders['diagnosis'] = le_diagnosis
        
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
            max_depth=8,
            min_samples_split=5,
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
        
        # Create DataFrame from input
        input_data = pd.DataFrame([patient_data])
        
        # Encode gender
        if 'gender' in self.label_encoders:
            input_data['gender'] = self.label_encoders['gender'].transform(input_data['gender'])
            
        # Ensure correct column order
        input_data = input_data[self.feature_names]
        
        prediction = self.model.predict(input_data)[0]
        probabilities = self.model.predict_proba(input_data)[0]
        
        diagnosis = self.label_encoders['diagnosis'].inverse_transform([prediction])[0]
        
        # Map probabilities to class names
        prob_dict = {}
        for i, prob in enumerate(probabilities):
            # Get class name from encoder
            class_idx = self.model.classes_[i]
            class_name = self.label_encoders['diagnosis'].inverse_transform([class_idx])[0]
            prob_dict[class_name] = float(prob)
        
        return diagnosis, prob_dict
    
    def visualize_tree(self):
        if not self.model:
            return None
            
        plt.figure(figsize=(20, 10))
        plot_tree(self.model,
                 feature_names=self.feature_names,
                 class_names=self.label_encoders['diagnosis'].classes_,
                 filled=True,
                 rounded=True,
                 fontsize=8)
        
        plt.title("Arbre de Décision - Diagnostic Médical (Analyses)")
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