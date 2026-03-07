import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth endpoints
export const login = async (email, password) => {
  try {
    const response = await api.post('/login', { email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const register = async (name, email, password) => {
  try {
    const response = await api.post('/register', { name, email, password });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// Marketplace endpoints
export const sellCrop = async (cropData) => {
  try {
    const response = await api.post('/sell-crop', cropData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const buyCrops = async () => {
  try {
    const response = await api.get('/buy-crops');
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

// AI Prediction endpoint
export const predictDisease = async (imageUri) => {
  try {
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'crop_image.jpg',
    });

    const response = await api.post('/predict', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export default api;
