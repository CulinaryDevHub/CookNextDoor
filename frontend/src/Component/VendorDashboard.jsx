import  { useState, useEffect, useCallback } from 'react';
// import { getVendorMenu, addDish, updateDish, deleteDish, getVendorOrders} from '../api';
import '../styles/VendorDashboard.css';
import { useParams } from 'react-router-dom';
import Optimisation from '../pages/Optimisation/optimisation';
import useVendorContext from '../context/VendorContext';

const VendorDashboard = () => {
  const { getVendorMenu, addDish, updateDish, deleteDish, getVendorOrders} = useVendorContext();
  const { vendorId } = useParams();
  const [menu, setMenu] = useState([]);
  const [orders, setOrders] = useState([]);
  const [newDish, setNewDish] = useState({ name: '', price: '', description: '', ingredients: '' });
  const [editDish, setEditDish] = useState(null); 
  const [updatedDish, setUpdatedDish] = useState({ name: '', price: '', description: '', ingredients: '' });
  // const [vendorInfo, setVendorInfo] = useState(null); 
   

  // const fetchVendorInfo = useCallback(async () => {
  //   try {
  //     const response = await getVendorInfo(vendorId);
  //     setVendorInfo(response.data);  
  //   } catch (error) {
  //     console.error('Error fetching vendor info', error);
  //   }
  // }, [vendorId]);


  const fetchMenu = useCallback(async () => {
    try {
      const response = await getVendorMenu(vendorId);
      console.log(response.data);
      setMenu(response.data);
    } catch (error) {
      console.error('Error fetching menu', error);
    }
  }, [vendorId]);

  const fetchOrders = useCallback(async () => {
    try {
      const response = await getVendorOrders(vendorId);
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching orders', error);
    }
  }, [vendorId]);

  useEffect(() => {
    // fetchVendorInfo();
    fetchMenu();
    fetchOrders();
  }, [fetchMenu, fetchOrders]);

  const handleAddDish = async () => {
    if (newDish.name.trim() === '' || newDish.price <= 0) {
      alert('Please enter a valid dish name and price');
      return;
    }

    try {
      await addDish({
        dish_name: newDish.name,
        price: parseFloat(newDish.price),
        vendor_id: vendorId,
        description: newDish.description,
        ingredients: newDish.ingredients
      });
      fetchMenu(); 
      setNewDish({ name: '', price: '', description: '', ingredients: '' }); 
    } catch (error) {
      console.error('Error adding dish', error);
    }
  };

  const handleDeleteDish = async (dishId) => {
    if (window.confirm('Are you sure you want to delete this dish?')) {
      try {
        await deleteDish(dishId);
        fetchMenu(); // Refresh the menu after deleting a dish
      } catch (error) {
        console.error('Error deleting dish', error);
      }
    }
  };

  const handleEditDish = (dish) => {
    setEditDish(dish.dish_id);
    setUpdatedDish({ name: dish.dish_name, price: dish.price, description: dish.description, ingredients: dish.ingredients }); // Populate the edit form with the current values
  };

  const handleUpdateDish = async (dishId) => {
    if (updatedDish.name.trim() === '' || updatedDish.price <= 0) {
      alert('Please enter a valid dish name and price');
      return;
    }

    try {
      await updateDish(dishId, {
        dish_name: updatedDish.name,
        price: parseFloat(updatedDish.price),
        description: updatedDish.description,
        ingredients: updatedDish.ingredients
      });
      fetchMenu();
      setEditDish(null);
    } catch (error) {
      console.error('Error updating dish', error);
    }
  };

  return (
    <div className="vendor-dashboard-container">
      <h2 className="vendor-dashboard-title">Vendor Dashboard</h2>
      <Optimisation/>

      {/* Vendor Info Section
      <div className="vendor-info-section">
        {vendorInfo ? (
          <div className="vendor-info">
            <h3>Welcome, {vendorInfo.name}!</h3>
            <p>Email: {vendorInfo.email}</p>
            <p>Location: {vendorInfo.location}</p>
          </div>
        ) : (
          <p>Loading vendor information...</p>
        )}
      </div> */}

      {/* Menu Section */}
      <div className="menu-section">
        <h3 className="section-title">Your Menu</h3>
        {menu.length > 0 ? (
          <ul className="menu-list">
            {menu.map((dish) => (
              <li key={dish.dish_id} className="menu-item">
                {editDish === dish.dish_id ? (
                  <>
                    <input
                      type="text"
                      value={updatedDish.name}
                      onChange={(e) => setUpdatedDish({ ...updatedDish, name: e.target.value })}
                      placeholder="Dish name"
                      className="input-field"
                    />
                    <input
                      type="number"
                      value={updatedDish.price}
                      onChange={(e) => setUpdatedDish({ ...updatedDish, price: e.target.value })}
                      placeholder="Price"
                      className="input-field"
                    />
                    <input
                      type="text"
                      value={updatedDish.description}
                      onChange={(e) => setUpdatedDish({ ...updatedDish, description: e.target.value })}
                      placeholder="Description"
                      className="input-field"
                    />
                    <input
                      type="text"
                      value={updatedDish.ingredients}
                      onChange={(e) => setUpdatedDish({ ...updatedDish, ingredients: e.target.value })}
                      placeholder="Ingredients"
                      className="input-field"
                    />
                    <button
                      onClick={() => handleUpdateDish(dish.dish_id)}
                      className="save-button"
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setEditDish(null)}
                      className="cancel-button"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <span><strong>Name:</strong> {dish.dish_name}</span> <br />
                    <span><strong>Price:</strong> Rs{dish.price}</span> <br />
                    <span><strong>Description:</strong> {dish.description || "No description provided"}</span> <br />
                    <span><strong>Ingredients:</strong> {dish.ingredients || "No ingredients provided"}</span> <br />
                    <button
                      className="edit-button"
                      onClick={() => handleEditDish(dish)}
                    >
                      Edit
                    </button>
                    <button
                      className="delete-button"
                      onClick={() => handleDeleteDish(dish.dish_id)}
                    >
                      Delete
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty-message">No dishes available. Add some dishes to your menu.</p>
        )}
        <div className="add-dish-form">
          <input
            type="text"
            value={newDish.name}
            onChange={(e) => setNewDish({ ...newDish, name: e.target.value })}
            placeholder="Dish name"
            className="input-field"
          />
          <input
            type="number"
            value={newDish.price}
            onChange={(e) => setNewDish({ ...newDish, price: e.target.value })}
            placeholder="Price"
            className="input-field"
          />
          <input
            type="text"
            value={newDish.description}
            onChange={(e) => setNewDish({ ...newDish, description: e.target.value })}
            placeholder="Description"
            className="input-field"
          />
          <input
            type="text"
            value={newDish.ingredients}
            onChange={(e) => setNewDish({ ...newDish, ingredients: e.target.value })}
            placeholder="Ingredients"
            className="input-field"
          />
          <button onClick={handleAddDish} className="add-button">Add Dish</button>
        </div>
      </div>

      {/* Orders Section */}
      <div className="orders-section">
        <h3 className="section-title">Orders</h3>
        {orders.length > 0 ? (
          <ul className="orders-list">
            {orders.map((order) => (
              <li key={order.order_id} className="order-item">
                <span>Order #{order.order_id} - Total: Rs{order.total_price}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty-message">No orders available at the moment.</p>
        )}
      </div>
    </div>
  );
};

export default VendorDashboard;
