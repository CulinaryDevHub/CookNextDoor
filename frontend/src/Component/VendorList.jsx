
import React, { useState, useEffect } from 'react';
import { getAllVendors } from '../api';
import { useNavigate } from 'react-router-dom';
import '../styles/VendorDetails.css';


const VendorList = () => {
  const [vendors, setVendors] = useState([]);
  const navigate = useNavigate(); 

  useEffect(() => {
    fetchVendors();
  }, []);

  const fetchVendors = async () => {
    try {
      const response = await getAllVendors();
      setVendors(response.data);
    } catch (error) {
      console.error('Error fetching vendors', error);
    }
  };

  const handleViewVendor = (vendorId) => {
    navigate(`/vendor/${vendorId}`); 
  };

  return (
    <div className="vendor-list-container">
      <h1 className="vendor-list-title">Vendors List</h1>
      <ul className="vendor-list">
        {vendors.map((vendor, index) => (
          <li key={index} className="vendor-item">
            <h2>{vendor.first_name} {vendor.last_name}</h2>
            <p>{vendor.email}</p>
            <button onClick={() => handleViewVendor(vendor.vendor_id)}>View Menu</button>

          </li>
        ))}
      </ul>
    </div>
  );
};


export default VendorList;
