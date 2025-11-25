import { useState } from 'react';
import Header from './components/Header';
import DiagnosticForm from './components/DiagnosticForm';
import HistoryView from './components/HistoryView';
import ResultsModal from './components/ResultsModal';
import './index.css';

function App() {
  const [activeTab, setActiveTab] = useState('diagnostic');
  const [showResults, setShowResults] = useState(false);
  const [diagnosisResult, setDiagnosisResult] = useState(null);

  const handleDiagnosisComplete = (result) => {
    setDiagnosisResult(result);
    setShowResults(true);
  };

  const handleCloseResults = () => {
    setShowResults(false);
    setActiveTab('historic'); //Switch to history tab after diagnosis
  };

  const handleNewDiagnosis = () => {
    setShowResults(false);
    setActiveTab('diagnostic');
    setDiagnosisResult(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('diagnostic')}
            className={`tab-button ${activeTab === 'diagnostic' ? 'tab-active' : 'tab-inactive'
              }`}
          >
            <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            Diagnostic
          </button>

          <button
            onClick={() => setActiveTab('historic')}
            className={`tab-button ${activeTab === 'historic' ? 'tab-active' : 'tab-inactive'
              }`}
          >
            <svg className="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Historique
          </button>
        </div>

        {/* Content */}
        {activeTab === 'diagnostic' && (
          <DiagnosticForm onDiagnosisComplete={handleDiagnosisComplete} />
        )}

        {activeTab === 'historic' && (
          <HistoryView />
        )}
      </div>

      {/* Results Modal */}
      {showResults && diagnosisResult && (
        <ResultsModal
          result={diagnosisResult}
          onClose={handleCloseResults}
          onNewDiagnosis={handleNewDiagnosis}
        />
      )}
    </div>
  );
}

export default App;
