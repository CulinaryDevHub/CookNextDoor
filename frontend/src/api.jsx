import axios from 'axios';


// Create an axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to get token from localStorage and return headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  if (token) {
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  } else {
    console.error("No token found");
    return {
      'Content-Type': 'application/json',
    };
  }
};

// API methods with explicit headers

// Get Vendor Menu
export const getVendorMenu = (vendorId) => {
  return api.get(`vendor/menu/${vendorId}`, {
    // headers: getAuthHeaders(),
  });
};

// Add a new dish
export const addDish = (dishData) => {
  return api.post(`menu/add`, dishData, {
    headers: getAuthHeaders(),
  });
};

// Update a dish
export const updateDish = (dishId, dishData) => {
  return api.put(`menu/update/${dishId}`, dishData, {
    headers: getAuthHeaders(),
  });
};

// Delete a dish
export const deleteDish = (dishId) => {
  return api.delete(`vendor/menu/delete/${dishId}`, {
    headers: getAuthHeaders(),
  });
};

// Get vendor orders
export const getVendorOrders = (vendorId) => {
  return api.get(`orders`, {
    headers: getAuthHeaders(),
  });
};

// Get all vendors (customer side)
export const getAllVendors = () => {
  return api.get(`/vendors`, {
    headers: getAuthHeaders(),
  });
};

// Get vendor menu for customer
export const getVendorMenuForCustomer = (vendorId) => {
  return api.get(`/vendor/menu/${vendorId}`, {
    headers: getAuthHeaders(),
  });
};

// Get all dishes for customer
export const getAllDishes = () => {
  return api.get(`customer/dishes`, {
    headers: getAuthHeaders(),
  });
};


