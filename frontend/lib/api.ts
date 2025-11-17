import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (email: string, password: string) =>
    api.post('/auth/login/json', { email, password }),
  getCurrentUser: () => api.get('/auth/me'),
};

// Questions API
export const questionsAPI = {
  list: (params?: any) => api.get('/questions/', { params }),
  get: (id: string) => api.get(`/questions/${id}`),
};

// Practice API
export const practiceAPI = {
  start: (questionId: string) =>
    api.post('/practice/start', { question_id: questionId, status: 'in_progress' }),
  submit: (questionId: string, code: string, language: string) =>
    api.post('/practice/submit', { question_id: questionId, code, language }),
  getHint: (questionId: string, currentCode: string, hintNumber: number) =>
    api.post('/practice/hint', {
      question_id: questionId,
      current_code: currentCode,
      hint_number: hintNumber,
    }),
};

// Progress API
export const progressAPI = {
  getDashboard: () => api.get('/progress/dashboard'),
  getSkills: () => api.get('/progress/skills'),
};
