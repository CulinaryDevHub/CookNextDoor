// src/components/VendorDetails.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getVendorMenuForCustomer } from '../api';
import '../styles/VendorDetails.css'; 

const VendorDetails = () => {
  const { vendorId } = useParams();
  const [menu, setMenu] = useState([]);

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await getVendorMenuForCustomer(vendorId);
        setMenu(response.data);
      } catch (error) {
        console.error('Error fetching vendor menu', error);
      }
    };

    fetchMenu();
  }, [vendorId]);

  return (
    <div className="vendor-details-container">
      <h1 className="vendor-details-title">Vendor Menu</h1>
      <ul className="vendor-menu-list">
        {menu.map((dish) => (
          <li key={dish.dish_id} className="vendor-menu-item">
            <h2>{dish.dish_name}</h2>
            <p className="menu-price">${dish.price}</p>
            <p>{dish.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VendorDetails;
