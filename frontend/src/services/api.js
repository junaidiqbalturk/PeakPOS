import axios from "axios";

// Match your Flask app's route structure
const API_URL = "http://127.0.0.1:5000/api/";

// Create Axios Instance with correct baseURL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Improved token handling in the interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response interceptor for handling auth errors consistently
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Authentication error: Your session might have expired");
    }
    return Promise.reject(error);
  }
);

// Helper to extract clean error message from backend
const extractError = (error, defaultMsg) => {
  if (error.response && error.response.data) {
    const data = error.response.data;
    const msg = data.error || data.message || `${defaultMsg} (${error.response.status})`;
    const err = new Error(msg);
    err.error = msg;
    err.response = error.response;
    return err;
  }
  if (error.request) {
    const err = new Error("No response from server. Please check your internet connection.");
    err.error = err.message;
    return err;
  }
  const err = new Error(error.message || defaultMsg);
  err.error = err.message;
  return err;
};

// Authentication Functions

// Login User
export const loginUser = async (email, password) => {
  try {
    const response = await api.post("/auth/login", { email, password });

    localStorage.setItem("token", response.data.token);
    localStorage.setItem("role", response.data.role);
    localStorage.setItem("isAuthenticated", "true");

    return response.data;
  } catch (error) {
    throw extractError(error, "Login failed");
  }
};

// Signup User
export const signupUser = async (username, email, password) => {
  try {
    const response = await api.post("/auth/signup", {
      username,
      email,
      password
    });
    return response.data;
  } catch (error) {
    throw extractError(error, "Signup failed");
  }
};

// Get User Info (Protected Route)
export const getUserInfo = async () => {
  try {
    const response = await api.get("/auth/user/me");
    return response.data;
  } catch (error) {
    throw extractError(error, "Failed to fetch user data");
  }
};

// Logout Function
export const logoutUser = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("isAuthenticated");
};

// Helper method to check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem("token");
  return !!token;
};

export default api;
