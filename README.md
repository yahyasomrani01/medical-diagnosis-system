# 🏥 Medical Diagnosis System

A Django-based machine learning web application that predicts medical conditions based on patient symptoms and vital signs using Decision Tree Classification.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2.7-green)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-1.7.2-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🤖 AI-Powered Diagnosis**: Machine learning model trained to predict 5 types of medical conditions
- **📊 Visual Analytics**: Interactive decision tree visualization and feature importance charts
- **💉 Patient Data Management**: Store and retrieve patient predictions from database
- **📈 Probability Analysis**: View confidence scores for all possible diagnoses
- **🌐 RESTful API**: JSON API endpoint for external integrations
- **🎨 Modern UI**: Clean, responsive Bootstrap-based interface in French
- **🔄 Real-time Predictions**: Instant diagnosis based on input symptoms and vitals

## 🎯 Supported Diagnoses

The system can predict the following conditions:

1. **SAIN** - Healthy Patient (Patient Sain)
2. **DIABETE** - Diabetes (Diabète)
3. **HYPER** - Hypertension
4. **CARDIAC** - Cardiac Problems (Problème Cardiaque)
5. **RESPIRATORY** - Respiratory Problems (Problème Respiratoire)

## 🖼️ Demo

### Training the Model

Train the decision tree classifier with 200 sample patient records achieving ~90% accuracy.

### Making Predictions

Input patient symptoms and vitals to receive instant diagnosis with probability scores.

### Results Display

View detailed diagnosis with probability breakdown for all conditions.

## 🛠️ Technologies

### Backend

- **Django 4.2.7** - Web framework
- **Python 3.13** - Programming language
- **SQLite** - Database

### Machine Learning

- **scikit-learn 1.7.2** - Decision Tree Classifier
- **pandas 2.3.3** - Data manipulation
- **numpy 2.3.5** - Numerical computing

### Visualization

- **matplotlib 3.10.7** - Decision tree plots
- **seaborn 0.13.2** - Statistical visualizations

### Frontend

- **Bootstrap 5.1.3** - UI framework
- **HTML5/CSS3** - Markup and styling

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/medical-diagnosis.git
   cd medical-diagnosis
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\\Scripts\\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 🚀 Usage

### Training the Model

1. Navigate to `http://127.0.0.1:8000/train/`
2. Click "Entraîner le Modèle" (Train Model)
3. View the accuracy score and decision tree visualization

### Making a Diagnosis

1. Navigate to `http://127.0.0.1:8000/predict/`
2. Fill in patient information:
   - **Demographics**: Age, Gender
   - **Symptoms**: Fever, Cough, Chest Pain, etc.
   - **Vital Signs**: Blood Pressure, Cholesterol, Blood Sugar
   - **Risk Factors**: Smoking, Obesity, Family History
3. Click "Analyser le Diagnostic" (Analyze Diagnosis)
4. View the prediction results with probability scores

### Using the API

Make POST requests to `/api/predict/` with JSON data:

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "age": 55,
    "gender": "M",
    "fever": true,
    "cough": true,
    "chest_pain": true,
    "shortness_breath": true,
    "fatigue": false,
    "headache": false,
    "nausea": false,
    "blood_pressure": 160,
    "cholesterol": 250,
    "blood_sugar": 95,
    "smoking": true,
    "obesity": false,
    "family_history": true
  }'
```

Response:

```json
{
  "diagnosis": "Problème Cardiaque",
  "probabilities": {
    "SAIN": 0.0,
    "DIABETE": 0.0,
    "HYPER": 0.0,
    "CARDIAC": 1.0,
    "RESPIRATORY": 0.0
  },
  "success": true
}
```

## 🧠 Model Details

### Algorithm

- **Type**: Decision Tree Classifier
- **Criterion**: Entropy (Information Gain)
- **Max Depth**: 5
- **Min Samples Split**: 10
- **Training Accuracy**: ~90%

### Features (15 total)

**Demographics**

- Age (18-80 years)
- Gender (M/F)

**Symptoms** (Binary: 0/1)

- Fever
- Cough
- Chest Pain
- Shortness of Breath
- Fatigue
- Headache
- Nausea

**Vital Signs**

- Blood Pressure (90-180 mmHg)
- Cholesterol (150-300 mg/dL)
- Blood Sugar (70-200 mg/dL)

**Risk Factors** (Binary: 0/1)

- Smoking
- Obesity
- Family History

### Training Data

- 200 synthetic patient records
- Stratified train-test split (80/20)
- Balanced across 5 diagnosis classes

## 📁 Project Structure

```
medical-diagnosis/
├── medical_app/              # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── medical_app/
│   │       ├── index.html
│   │       ├── predict.html
│   │       ├── results.html
│   │       ├── dataset.html
│   │       └── model_info.html
│   ├── admin.py             # Django admin config
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── ml_model.py          # ML model class
│   ├── models.py            # Database models
│   ├── urls.py              # URL routing
│   └── views.py             # View functions
├── medical_project/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## 🔌 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/train/` | GET/POST | Train model page |
| `/predict/` | GET/POST | Prediction form |
| `/results/<id>/` | GET | View patient results |
| `/model-info/` | GET | Model visualization |
| `/api/predict/` | POST | JSON API for predictions |

### API Request Format

```json
{
  "age": 55,
  "gender": "M",
  "fever": true,
  "cough": false,
  "chest_pain": true,
  "shortness_breath": true,
  "fatigue": false,
  "headache": false,
  "nausea": false,
  "blood_pressure": 160,
  "cholesterol": 250,
  "blood_sugar": 95,
  "smoking": true,
  "obesity": false,
  "family_history": true
}
```

### API Response Format

```json
{
  "diagnosis": "Problème Cardiaque",
  "probabilities": {
    "SAIN": 0.0,
    "DIABETE": 0.0,
    "HYPER": 0.0,
    "CARDIAC": 1.0,
    "RESPIRATORY": 0.0
  },
  "success": true
}
```

## 🐛 Known Issues & Fixes

### Issue: Matplotlib Crash on macOS

**Solution**: The application uses `matplotlib.use('Agg')` backend to prevent GUI-related crashes.

### Issue: Database Locked

**Solution**: SQLite is configured for single-user development. For production, use PostgreSQL or MySQL.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**This application is for educational purposes only.** It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions regarding medical conditions.

## 👨‍💻 Author

Created with ❤️ by Yahya Somrani

## 🙏 Acknowledgments

- Decision Tree algorithm from scikit-learn
- Bootstrap for the UI framework
- Django for the robust web framework
- The Python community for excellent libraries

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Made with Python & Django** | **Powered by Machine Learning** | **Built for Healthcare Education**
