# Medical Diagnosis Frontend (React + Vite)

Modern React frontend for the Medical Diagnosis System.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Start Development Server

```bash
npm run dev
```

App will run on `http://localhost:5173`

## Build for Production

```bash
npm run build
```

Build files will be in `dist/` directory.

## Features

- ✨ Modern single-page application
- 🎨 Beautiful Tailwind CSS design
- 📱 Fully responsive
- ⚡ Fast Vite dev server
- 🔄 Real-time API communication
- 🎯 Tab navigation (Diagnostic / History)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # App header
│   │   ├── DiagnosticForm.jsx  # Main diagnostic form
│   │   ├── HistoryView.jsx     # Past diagnoses
│   │   └── ResultsModal.jsx    # Results popup
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.jsx                # Main app component
│   └── index.css              # Tailwind styles
├── package.json              # Dependencies
├── tailwind.config.js        # Tailwind configuration
└── vite.config.js           # Vite configuration
```

## Usage

1. **Train Model** (one-time setup):
   - Backend must train the model first via API

2. **Make Diagnosis**:
   - Fill in patient information
   - Enter symptoms and vitals
   - Click "Analyser et Diagnostiquer"
   - View results in modal

3. **View History**:
   - Click "Historique" tab
   - See all past diagnoses

## UI Design

- **Primary Color**: Blue (#1E88E5)
- **Style**: Modern, clean, card-based
- **Components**: Headers, forms, modals, tabs
- **Responsive**: Works on all screen sizes
