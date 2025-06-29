import  { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllVendors } from '../api'; 
import '../styles/CustomerPage.css'; 
import Recommendation from '../pages/Recommendation/recommendation';



const CustomerPage = () => {
  const [vendors, setVendors] = useState([]);
  const navigate = useNavigate(); 

  useEffect(() => {
    const fetchVendors = async () => {
      try {
        const response = await getAllVendors();
        setVendors(response.data);
      } catch (error) {
        console.error('Error fetching vendors', error);
      }
    };

    fetchVendors();
  }, []);

  // Function to navigate to the vendor's menu page
  const handleViewMenu = (vendorId) => {
    navigate(`/vendor/${vendorId}`);
  };

  return (
    <div className="customer-page-container">
    <Recommendation/>
      <h1 className="customer-page-title">Available Vendors</h1>
      <ul className="vendor-list">
        {vendors.length > 0 ? (
          vendors.map((vendor) => (
            <li key={vendor.vendor_id} className="vendor-item">
              <h2 className="vendor-name">{vendor.firstname}</h2>
              <p className="vendor-description">{vendor.lastname}</p>
              <p className="vendor-location">Location: {vendor.address}</p>
              {/* Add a button to view the vendor's menu */}
              <button onClick={() => handleViewMenu(vendor.vendor_id)} className="view-menu-button">
                View Menu
              </button>
            </li>
          ))
        ) : (
          <p>No vendors available at the moment.</p>
        )}
      </ul>
    </div>
  );
};

export default CustomerPage;
