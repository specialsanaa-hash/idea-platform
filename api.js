/**
 * مكتبة API للتواصل مع خادم Django
 */

import axios from 'axios';

// إعداد axios الأساسي
const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة token للطلبات
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// معالجة الاستجابات والأخطاء
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // فشل في تجديد الـ token، إعادة توجيه لصفحة تسجيل الدخول
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// دوال المصادقة
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post('/token/', credentials);
    const { access, refresh } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getCurrentUser: () => api.get('/users/me/'),

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

// دوال المستخدمين
export const usersAPI = {
  getUsers: (params) => api.get('/users/', { params }),
  getUser: (id) => api.get(`/users/${id}/`),
  createUser: (data) => api.post('/users/', data),
  updateUser: (id, data) => api.put(`/users/${id}/`, data),
  deleteUser: (id) => api.delete(`/users/${id}/`),
  getUserProfile: (id) => api.get(`/users/${id}/profile/`),
  updateUserProfile: (id, data) => api.put(`/users/${id}/profile/`, data),
};

// دوال العملاء
export const clientsAPI = {
  getClients: (params) => api.get('/crm/clients/', { params }),
  getClient: (id) => api.get(`/crm/clients/${id}/`),
  createClient: (data) => api.post('/crm/clients/', data),
  updateClient: (id, data) => api.put(`/crm/clients/${id}/`, data),
  deleteClient: (id) => api.delete(`/crm/clients/${id}/`),
  getClientProjects: (id) => api.get(`/crm/clients/${id}/projects/`),
  getClientInvoices: (id) => api.get(`/crm/clients/${id}/invoices/`),
};

// دوال المشاريع
export const projectsAPI = {
  getProjects: (params) => api.get('/projects/', { params }),
  getProject: (id) => api.get(`/projects/${id}/`),
  createProject: (data) => api.post('/projects/', data),
  updateProject: (id, data) => api.put(`/projects/${id}/`, data),
  deleteProject: (id) => api.delete(`/projects/${id}/`),
  createFromTemplate: (data) => api.post('/projects/from-template/', data),
  getProjectTasks: (id) => api.get(`/projects/${id}/tasks/`),
  getDashboardStats: () => api.get('/projects/dashboard/stats/'),
};

// دوال المهام
export const tasksAPI = {
  getTasks: (params) => api.get('/projects/tasks/', { params }),
  getTask: (id) => api.get(`/projects/tasks/${id}/`),
  createTask: (data) => api.post('/projects/tasks/', data),
  updateTask: (id, data) => api.put(`/projects/tasks/${id}/`, data),
  deleteTask: (id) => api.delete(`/projects/tasks/${id}/`),
  completeTask: (id) => api.post(`/projects/tasks/${id}/complete/`),
  getMyTasks: () => api.get('/projects/tasks/my-tasks/'),
};

// دوال القوالب
export const templatesAPI = {
  getProjectTemplates: (params) => api.get('/projects/templates/', { params }),
  getProjectTemplate: (id) => api.get(`/projects/templates/${id}/`),
  createProjectTemplate: (data) => api.post('/projects/templates/', data),
  updateProjectTemplate: (id, data) => api.put(`/projects/templates/${id}/`, data),
  deleteProjectTemplate: (id) => api.delete(`/projects/templates/${id}/`),
  
  getTaskTemplates: (params) => api.get('/projects/task-templates/', { params }),
  getTaskTemplate: (id) => api.get(`/projects/task-templates/${id}/`),
  createTaskTemplate: (data) => api.post('/projects/task-templates/', data),
  updateTaskTemplate: (id, data) => api.put(`/projects/task-templates/${id}/`, data),
  deleteTaskTemplate: (id) => api.delete(`/projects/task-templates/${id}/`),
};

// دوال الفواتير
export const invoicesAPI = {
  getInvoices: (params) => api.get('/crm/invoices/', { params }),
  getInvoice: (id) => api.get(`/crm/invoices/${id}/`),
  createInvoice: (data) => api.post('/crm/invoices/', data),
  updateInvoice: (id, data) => api.put(`/crm/invoices/${id}/`, data),
  deleteInvoice: (id) => api.delete(`/crm/invoices/${id}/`),
  markAsPaid: (id) => api.post(`/crm/invoices/${id}/mark-paid/`),
  sendInvoice: (id) => api.post(`/crm/invoices/${id}/send/`),
};

// دوال التفاعلات
export const interactionsAPI = {
  getInteractions: (params) => api.get('/crm/interactions/', { params }),
  getInteraction: (id) => api.get(`/crm/interactions/${id}/`),
  createInteraction: (data) => api.post('/crm/interactions/', data),
  updateInteraction: (id, data) => api.put(`/crm/interactions/${id}/`, data),
  deleteInteraction: (id) => api.delete(`/crm/interactions/${id}/`),
};

export default api;

