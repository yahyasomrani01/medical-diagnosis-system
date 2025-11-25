import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const medicalAPI = {
    // Train the ML model
    trainModel: async () => {
        const response = await api.post('/train/');
        return response.data;
    },

    // Make a prediction
    predict: async (patientData) => {
        const response = await api.post('/predict/', patientData);
        return response.data;
    },

    // Get prediction history
    getHistory: async () => {
        const response = await api.get('/history/');
        return response.data;
    },

    // Get specific result
    getResult: async (id) => {
        const response = await api.get(`/results/${id}/`);
        return response.data;
    },
};

export default api;
