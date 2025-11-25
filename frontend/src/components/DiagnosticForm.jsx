import { useState } from 'react';
import { medicalAPI } from '../services/api';

const DiagnosticForm = ({ onDiagnosisComplete }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        age: '',
        gender: 'M',
        // Lab Results
        glucose: '',
        cholesterol: '',
        triglycerides: '',
        creatinine: '',
        uree: '',
        uric_acid: '',
        got: '',
        gpt: '',
        bilirubin: '',
        // Risk factors
        smoking: false,
        obesity: false,
        family_history: false,
    });

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            // Prepare data for API
            const apiData = {
                age: parseInt(formData.age),
                gender: formData.gender,
                glucose: parseFloat(formData.glucose),
                cholesterol: parseFloat(formData.cholesterol),
                triglycerides: parseFloat(formData.triglycerides),
                creatinine: parseFloat(formData.creatinine),
                uree: parseFloat(formData.uree),
                uric_acid: parseFloat(formData.uric_acid),
                got: parseFloat(formData.got),
                gpt: parseFloat(formData.gpt),
                bilirubin: parseFloat(formData.bilirubin),
                smoking: formData.smoking,
                obesity: formData.obesity,
                family_history: formData.family_history,
            };

            const result = await medicalAPI.predict(apiData);
            // Pass patient name to result for PDF generation
            onDiagnosisComplete({ ...result, patientName: formData.name });
        } catch (error) {
            console.error('Error making prediction:', error);
            alert('Erreur lors de la prédiction. Veuillez vérifier les valeurs.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card max-w-6xl mx-auto">
            <div className="mb-6">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Nouvelle Analyse Laboratoire
                </h2>
                <p className="text-gray-600 text-sm mt-1">
                    Entrez les résultats d'analyses sanguines pour obtenir un diagnostic
                </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
                {/* Patient Information */}
                <div>
                    <h3 className="font-semibold text-gray-900 mb-4 border-b pb-2">Informations Patient</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Nom complet</label>
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Âge</label>
                            <input
                                type="number"
                                name="age"
                                value={formData.age}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Genre</label>
                            <select
                                name="gender"
                                value={formData.gender}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            >
                                <option value="M">Masculin</option>
                                <option value="F">Féminin</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Metabolic Panel */}
                <div>
                    <h3 className="font-semibold text-gray-900 mb-4 border-b pb-2">Bilan Métabolique & Lipidique</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Glucose (mmol/L)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="glucose"
                                value={formData.glucose}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 5.0"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Cholestérol (mmol/L)</label>
                            <input
                                type="number"
                                step="0.01"
                                name="cholesterol"
                                value={formData.cholesterol}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 4.5"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Triglycérides (mmol/L)</label>
                            <input
                                type="number"
                                step="0.01"
                                name="triglycerides"
                                value={formData.triglycerides}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 1.2"
                                required
                            />
                        </div>
                    </div>
                </div>

                {/* Kidney Function */}
                <div>
                    <h3 className="font-semibold text-gray-900 mb-4 border-b pb-2">Fonction Rénale</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Créatinine (µmol/L)</label>
                            <input
                                type="number"
                                step="1"
                                name="creatinine"
                                value={formData.creatinine}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 80"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Urée (mmol/L)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="uree"
                                value={formData.uree}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 5.0"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Acide Urique (µmol/L)</label>
                            <input
                                type="number"
                                step="1"
                                name="uric_acid"
                                value={formData.uric_acid}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 300"
                                required
                            />
                        </div>
                    </div>
                </div>

                {/* Liver Function */}
                <div>
                    <h3 className="font-semibold text-gray-900 mb-4 border-b pb-2">Fonction Hépatique</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">GOT (AST) (U/L)</label>
                            <input
                                type="number"
                                step="1"
                                name="got"
                                value={formData.got}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 25"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">GPT (ALT) (U/L)</label>
                            <input
                                type="number"
                                step="1"
                                name="gpt"
                                value={formData.gpt}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 25"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Bilirubine Totale (µmol/L)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="bilirubin"
                                value={formData.bilirubin}
                                onChange={handleInputChange}
                                className="input-field"
                                placeholder="Ex: 10"
                                required
                            />
                        </div>
                    </div>
                </div>

                {/* Risk Factors */}
                <div>
                    <h3 className="font-semibold text-gray-900 mb-4 border-b pb-2">Facteurs de Risque</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {[
                            { name: 'smoking', label: 'Fumeur' },
                            { name: 'obesity', label: 'Obésité' },
                            { name: 'family_history', label: 'Antécédents familiaux' },
                        ].map((risk) => (
                            <label key={risk.name} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors">
                                <input
                                    type="checkbox"
                                    name={risk.name}
                                    checked={formData[risk.name]}
                                    onChange={handleInputChange}
                                    className="w-5 h-5 text-primary-600 focus:ring-primary-500 rounded"
                                />
                                <span className="text-gray-700">{risk.label}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary"
                >
                    {loading ? (
                        <span className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Analyse en cours...
                        </span>
                    ) : (
                        'Analyser et Diagnostiquer'
                    )}
                </button>
            </form>
        </div>
    );
};

export default DiagnosticForm;
