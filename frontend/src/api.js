
import axios from 'axios';


const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api', 
  headers: {
    'Content-Type': 'application/json',
  },
});


export const getVendorMenu = (vendorId) => api.get(`vendor/menu/${vendorId}`);
export const addDish = (dishData) => api.post(`vendor/menu/add`, dishData);
export const updateDish = (dishId, dishData) => api.put(`vendor/menu/update/${dishId}`, dishData,{
  headers: {
    'Content-Type': 'application/json',
  },
});
export const deleteDish = (dishId) => api.delete(`vendor/menu/delete/${dishId}`);
export const getVendorOrders = (vendorId) => api.get(`vendor/orders/${vendorId}`);


export const getAllVendors = () => api.get(`/customer/vendors`);
export const getVendorMenuForCustomer = (vendorId) => api.get(`customer/vendor/menu/${vendorId}`);
export const getAllDishes = () => api.get(`customer/dishes`);