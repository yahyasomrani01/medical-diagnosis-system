# Medical Diagnosis Backend (Django REST API)

Django REST API backend for the Medical Diagnosis System.

## Tech Stack

- **Django 4.2.7** - Web framework
- **Django REST Framework** - REST API
- **scikit-learn** - Machine Learning
- **SQLite** - Database
- **ReportLab** - PDF Generation

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start Development Server

```bash
python manage.py runserver
```

Server will run on `http://localhost:8000`

### 5. Admin User Setup

To access the Django Admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

Or run the setup script (if available) to create a default admin:

- Username: `admin`
- Password: `admin123`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/train/` | POST | Train ML model |
| `/api/predict/` | POST | Make prediction |
| `/api/history/` | GET | Get all predictions |
| `/api/results/<id>/` | GET | Get specific result |
| `/api/prescription/<id>/` | GET | View prescription PDF (inline) |
| `/api/prescription-image/<id>/` | GET | View prescription as Image (PNG) |

## Test API

### Health Check

```bash
curl http://localhost:8000/api/health/
```

### Train Model

```bash
curl -X POST http://localhost:8000/api/train/
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "gender": "M",
    "glucose": 8.5,
    "cholesterol": 4.5,
    "triglycerides": 1.2,
    "creatinine": 80,
    "uree": 5.0,
    "uric_acid": 300,
    "got": 25,
    "gpt": 25,
    "bilirubin": 10,
    "smoking": false,
    "obesity": false,
    "family_history": false
  }'
```

## Project Structure

```
backend/
├── medical_app/          # Main Django app
│   ├── api_views.py      # REST API views
│   ├── serializers.py    # DRF serializers
│   ├── models.py         # Database models
│   ├── ml_model.py       # Machine Learning logic
│   ├── utils.py          # Utilities (PDF generation)
│   └── urls.py           # URL routing
├── medical_project/      # Django project settings
│   └── settings.py       # Configuration
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── db.sqlite3          # SQLite database
```

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## ML Model

The system uses a Decision Tree Classifier to predict diagnoses based on lab results:

- **Patient Sain** (Healthy)
- **Diabète** (Diabetes) - Based on Glucose
- **Hyperlipidémie** (High Lipids) - Based on Cholesterol/Triglycerides
- **Insuffisance Rénale** (Kidney Issues) - Based on Creatinine/Uree/Uric Acid
- **Insuffisance Hépatique** (Liver Issues) - Based on GOT/GPT/Bilirubin

Model accuracy: ~99%
