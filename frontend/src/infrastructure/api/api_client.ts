import axios from 'axios';
import { isTokenExpired } from '../../utils/jwt';

// Create a configured Axios instance
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to inject the JWT token if available
apiClient.interceptors.request.use(
  (config) => {
    // In a real application, you might want to get this from a secure cookie
    // or a context/store, but localStorage is common for initial setups.
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      
      if (token) {
        if (!isTokenExpired(token)) {
          config.headers.Authorization = `Bearer ${token}`;
        } else {
          // Token expirado, limpa do storage
          localStorage.removeItem('token');
        }
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for global error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access globally (e.g., redirect to login)
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        // Avoid redirect loop if already on login page
        if (window.location.pathname !== '/') {
          window.location.href = '/';
        }
      }
    }
    return Promise.reject(error);
  }
);
