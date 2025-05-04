import axios from "axios";

// UPDATED: Match your Flask app's route structure
const API_URL = "http://127.0.0.1:5000/api"; // Add /api to match your backend routes

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
    // Make sure the token format is exactly "Bearer {token}"
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Add response interceptor for handling auth errors consistently
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle authentication errors
    if (error.response && error.response.status === 401) {
      console.warn("Authentication error: Your session might have expired");

      // Optional: Redirect to login page if unauthorized
      // window.location.href = '/login';
    }

    return Promise.reject(error);
  }
);

// Authentication Functions

// Login User
export const loginUser = async (email, password) => {
  try {
    // Updated path: now goes to /api/auth/login to match your backend
    const response = await api.post("/auth/login", { email, password });

    localStorage.setItem("token", response.data.token); // Save JWT
    localStorage.setItem("role", response.data.role);   // Store role

    return response.data;
  } catch (error) {
    // Better error handling
    if (error.response) {
      throw error.response.data || {
        error: `Login failed (${error.response.status})`
      };
    } else if (error.request) {
      throw {
        error: "No response from server. Please check your internet connection."
      };
    } else {
      throw {
        error: error.message || "Login failed"
      };
    }
  }
};

// Signup User with improved error handling
export const signupUser = async (username, email, password) => {
  try {
    const response = await api.post("/auth/signup", {
      username,
      email,
      password
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw error.response.data || {
        error: `Signup failed (${error.response.status})`
      };
    } else if (error.request) {
      throw {
        error: "No response from server. Please check your internet connection."
      };
    } else {
      throw {
        error: error.message || "Signup failed"
      };
    }
  }
};

// Get User Info (Protected Route) with better error handling
export const getUserInfo = async () => {
  try {
    const response = await api.get("/auth/user/me");
    return response.data;
  } catch (error) {
    if (error.response) {
      if (error.response.status === 401) {
        throw { error: "Authentication required. Please login again." };
      }
      throw error.response.data || {
        error: `Failed to fetch user data (${error.response.status})`
      };
    } else if (error.request) {
      throw {
        error: "No response from server. Please check your internet connection."
      };
    } else {
      throw {
        error: error.message || "Failed to fetch user data"
      };
    }
  }
};

// Logout Function (Clears all auth-related items)
export const logoutUser = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("isAuthenticated");
  // Optionally redirect to login page
  // window.location.href = '/login';
};

// Helper method to check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem("token");
  return !!token; // Convert to boolean
};

export default api;