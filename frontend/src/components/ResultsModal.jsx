import React from 'react';

const ResultsModal = ({ result, onClose, onNewDiagnosis }) => {
    const diagnosisMap = {
        'SAIN': 'Patient Sain',
        'DIABETE': 'Diabète',
        'HYPERLIPIDEMIE': 'Hyperlipidémie',
        'RENAL': 'Insuffisance Rénale',
        'HEPATIQUE': 'Insuffisance Hépatique',
    };

    const diagnosisEmoji = {
        'SAIN': '✅',
        'DIABETE': '🩸',
        'HYPERLIPIDEMIE': '🍔',
        'RENAL': '💧',
        'HEPATIQUE': '🍺',
    };

    const handleDownloadPrescription = async () => {
        try {
            console.log("Requesting PDF from backend for patient ID:", result.id);

            // Use the API URL from environment or default
            const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

            const response = await fetch(`${API_URL}/prescription/${result.id}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/pdf',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            // Extract filename from header if possible, or construct one
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `Ordonnance_Patient_${result.id}.pdf`;

            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
                if (filenameMatch && filenameMatch.length === 2)
                    filename = filenameMatch[1];
            }

            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            console.log("PDF downloaded successfully");

        } catch (error) {
            console.error("Error downloading PDF:", error);
            alert("Erreur lors du téléchargement de l'ordonnance. Veuillez réessayer.");
        }
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-2xl w-full p-8 shadow-2xl">
                {/* Header */}
                <div className="text-center mb-8">
                    <div className="text-6xl mb-4">
                        {diagnosisEmoji[result.diagnosis] || '🏥'}
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        Résultat du Diagnostic
                    </h2>
                    <div className={`inline-block px-6 py-2 rounded-full text-lg font-semibold ${result.diagnosis === 'SAIN'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                        }`}>
                        {diagnosisMap[result.diagnosis] || result.diagnosis}
                    </div>
                </div>

                {/* Probabilities */}
                <div className="mb-8">
                    <h3 className="font-semibold text-gray-900 mb-4">Probabilités:</h3>
                    <div className="space-y-3">
                        {result.probabilities && Object.entries(result.probabilities).map(([key, value]) => (
                            <div key={key} className="flex items-center justify-between">
                                <span className="text-gray-700">{diagnosisMap[key] || key}</span>
                                <div className="flex items-center gap-3 flex-1 ml-4">
                                    <div className="flex-1 bg-gray-200 rounded-full h-2.5">
                                        <div
                                            className={`h-2.5 rounded-full ${value > 0.5 ? 'bg-primary-600' : 'bg-gray-400'
                                                }`}
                                            style={{ width: `${value * 100}%` }}
                                        ></div>
                                    </div>
                                    <span className="text-sm font-medium text-gray-900 w-16 text-right">
                                        {(value * 100).toFixed(0)}%
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-3">
                    <button
                        onClick={handleDownloadPrescription}
                        className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        Télécharger Ordonnance
                    </button>

                    <div className="flex gap-4">
                        <button
                            onClick={onNewDiagnosis}
                            className="flex-1 bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-all"
                        >
                            Nouveau Diagnostic
                        </button>
                        <button
                            onClick={onClose}
                            className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-lg transition-all"
                        >
                            Fermer
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultsModal;
