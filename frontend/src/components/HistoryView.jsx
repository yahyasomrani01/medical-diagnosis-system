import { useState, useEffect } from 'react';
import { medicalAPI } from '../services/api';

const HistoryView = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await medicalAPI.getHistory();
            setHistory(data);
        } catch (error) {
            console.error('Error fetching history:', error);
        } finally {
            setLoading(false);
        }
    };

    const diagnosisMap = {
        'SAIN': 'Patient Sain',
        'DIABETE': 'Diabète',
        'HYPER': 'Hypertension',
        'CARDIAC': 'Problème Cardiaque',
        'RESPIRATORY': 'Problème Respiratoire',
    };

    if (loading) {
        return (
            <div className="card text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="text-gray-600 mt-4">Chargement de l'historique...</p>
            </div>
        );
    }

    if (history.length === 0) {
        return (
            <div className="card text-center py-16">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun diagnostic dans l'historique</h3>
                <p className="text-gray-600">Les diagnostics apparaîtront ici après l'analyse</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Historique des Diagnostics</h2>

            {history.map((item) => (
                <div key={item.id} className="card hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <div className={`px-3 py-1 rounded-full text-sm font-medium ${item.diagnosis === 'SAIN'
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-orange-100 text-orange-800'
                                    }`}>
                                    {diagnosisMap[item.diagnosis] || item.diagnosis}
                                </div>
                                <span className="text-sm text-gray-500">
                                    {new Date(item.created_at).toLocaleDateString('fr-FR', {
                                        year: 'numeric',
                                        month: 'long',
                                        day: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </span>
                            </div>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
                                <div>
                                    <span className="text-gray-600">Âge:</span>
                                    <span className="ml-2 font-medium">{item.age} ans</span>
                                </div>
                                <div>
                                    <span className="text-gray-600">Genre:</span>
                                    <span className="ml-2 font-medium">{item.gender === 'M' ? 'Masculin' : 'Féminin'}</span>
                                </div>
                                <div>
                                    <span className="text-gray-600">TA:</span>
                                    <span className="ml-2 font-medium">{item.blood_pressure} mmHg</span>
                                </div>
                                <div>
                                    <span className="text-gray-600">Glycémie:</span>
                                    <span className="ml-2 font-medium">{item.blood_sugar} mg/dL</span>
                                </div>
                            </div>
                        </div>

                        <button className="ml-4 text-primary-600 hover:text-primary-700">
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default HistoryView;
