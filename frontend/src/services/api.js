import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api"; // Flask backend URL

// Create Axios Instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


// Automatically Attach JWT Token to Requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Authentication Functions

// Login User
export const loginUser = async (email, password) => {
  try {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("token", response.data.token); // Save JWT
    localStorage.setItem("role", response.data.role);   // Store role
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : "Login failed";
  }
};

// Signup User
export const signupUser = async (username, email, password) => {
  try {
    const response = await api.post("/auth/signup", { username, email, password });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : "Signup failed";
  }
};


// Get User Info (Protected Route)
export const getUserInfo = async () => {
  try {
    const response = await api.get("/auth/user/me");
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : "Failed to fetch user data";
  }
};

// Logout Function (Clears Token)
export const logoutUser = () => {
  localStorage.removeItem("token");
};

export default api;
