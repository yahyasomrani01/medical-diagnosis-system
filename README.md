# 🏥 Medical Diagnosis System

AI-powered medical diagnosis system with a modern React frontend and Django REST API backend.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2.7-green)
![React](https://img.shields.io/badge/React-18-blue)
![Vite](https://img.shields.io/badge/Vite-5-purple)

## 🎯 Overview

A full-stack medical diagnosis application that uses machine learning to predict medical conditions based on patient symptoms and vital signs.

**Diagnoses:** Patient Sain (Healthy), Diabète, Hypertension, Cardiac Issues, Respiratory Issues

**Accuracy:** ~90%

## 🏗️ Project Structure

```
medical-diagnosis/
├── frontend/          # React + Vite SPA
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service
│   │   └── App.jsx
│   ├── package.json
│   └── README.md
│
├── backend/           # Django REST API
│   ├── medical_app/       # Django application
│   ├── medical_project/   # Django settings
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
│
├── venv/              # Python virtual environment
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### 1. Clone Repository

```bash
git clone https://github.com/yahyasomrani01/medical-diagnosis-system.git
cd medical-diagnosis-system
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://localhost:8000`

### 3. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### 4. Train the Model

```bash
curl -X POST http://localhost:8000/api/train/
```

## 💻 Tech Stack

### Frontend

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Backend

- **Django 4.2.7** - Web framework
- **Django REST Framework** - API
- **scikit-learn** - ML model
- **SQLite** - Database

### Machine Learning

- **Algorithm:** Decision Tree Classifier
- **Features:** Age, gender, symptoms, vitals, risk factors (15 total)
- **Training Data:** 200 synthetic patient records

## 📋 Features

- ✨ Modern single-page React application
- 🎨 Beautiful Tailwind CSS design
- 🤖 AI-powered medical predictions
- 📊 Decision tree visualization
- 📱 Fully responsive
- 🔌 RESTful API
- 📈 Prediction history
- ⚡ Real-time diagnosis

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/train/` | POST | Train ML model |
| `/api/predict/` | POST | Make prediction |
| `/api/history/` | GET | Get all predictions |
| `/api/results/<id>/` | GET | Get specific result |

## 📸 Screenshots

### Diagnostic Form

Modern UI with patient information, symptoms, and vital signs input.

### Results Display

Clear diagnosis with probability breakdown for all conditions.

### History View

List of all past diagnoses with patient details.

## 🛠️ Development

### Backend Development

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Build for Production

```bash
# Frontend
cd frontend
npm run build

# Backend is production-ready with gunicorn
```

## 🚀 Deployment

### Frontend

- Deploy to Vercel, Netlify, or GitHub Pages
- Run `npm run build` first

### Backend

- Deploy to Railway, Heroku, or DigitalOcean
- Use `gunicorn` for production server
- Set environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS)

## ⚠️ Disclaimer

**This application is for educational purposes only.** It should not be used as a substitute for professional medical advice, diagnosis, or treatment.

## 📝 License

MIT License - see LICENSE file for details.

## 👨‍💻 Author

Created by Yahya Somrani

GitHub: [yahyasomrani01](https://github.com/yahyasomrani01)

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ using React, Django, and Machine Learning**
