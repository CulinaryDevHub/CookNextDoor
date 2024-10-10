import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const CartPage = () => {
  const [user, setUser] = useState({ name: '', address: '', phone: '' });
  const [cartItems, setCartItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch user details
    fetch('http://localhost:5000/api/getUserDetails')
      .then((response) => response.json())
      .then((data) => setUser(data))
      .catch((error) => console.error('Error fetching user details:', error));

    // Fetch cart items
    fetch('http://localhost:5000/api/getCartItems')
      .then((response) => response.json())
      .then((data) => {
        setCartItems(data.items);
        setTotalPrice(data.totalPrice);
      })
      .catch((error) => console.error('Error fetching cart items:', error));
  }, []);

  const handlePayment = () => {
    navigate('/order-confirmation');
  };

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f9f9f9', minHeight: '100vh' }}>
      {/* User Information Section */}
      <div style={{
        marginBottom: '30px',
        padding: '25px',
        border: '1px solid #ccc',
        borderRadius: '10px',
        backgroundColor: '#fff',
        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
      }}>
        <h2 style={{ color: '#2E7D32', textAlign: 'center', fontSize: '24px', marginBottom: '20px' }}>Customer Information</h2>
        <p style={{ fontSize: '18px' }}><strong>Name:</strong> {user.name}</p>
        <p style={{ fontSize: '18px' }}><strong>Address:</strong> {user.address}</p>
        <p style={{ fontSize: '18px' }}><strong>Phone:</strong> {user.phone}</p>
      </div>

      {/* Cart Items Section */}
      <div style={{
        padding: '25px',
        border: '1px solid #ccc',
        borderRadius: '10px',
        backgroundColor: '#fff',
        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
      }}>
        <h2 style={{ color: '#FF5C00', textAlign: 'center', fontSize: '24px', marginBottom: '20px' }}>Your Cart</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '30px' }}>
          <thead>
            <tr style={{ backgroundColor: '#FF5C00', color: '#fff' }}>
              <th style={{ padding: '12px', border: 'none', fontSize: '16px' }}>Order</th>
              <th style={{ padding: '12px', border: 'none', fontSize: '16px' }}>Quantity</th>
              <th style={{ padding: '12px', border: 'none', fontSize: '16px' }}>Price (₹)</th>
              <th style={{ padding: '12px', border: 'none', fontSize: '16px' }}>Total (₹)</th>
            </tr>
          </thead>
          <tbody>
            {cartItems.map((item, index) => (
              <tr key={index} style={{ backgroundColor: '#f9f9f9' }}>
                <td style={{ padding: '15px', textAlign: 'center', borderBottom: '1px solid #ccc' }}>{item.name}</td>
                <td style={{ padding: '15px', textAlign: 'center', borderBottom: '1px solid #ccc' }}>{item.quantity}</td>
                <td style={{ padding: '15px', textAlign: 'center', borderBottom: '1px solid #ccc' }}>₹{item.price}</td>
                <td style={{ padding: '15px', textAlign: 'center', borderBottom: '1px solid #ccc' }}>₹{(item.quantity * item.price).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Total Bill */}
        <h3 style={{ textAlign: 'right', fontSize: '22px', marginBottom: '30px', color: '#FF5C00' }}>Total Bill: ₹{totalPrice.toFixed(3)}</h3>

        {/* Pay using Cash Button */}
        <button
          onClick={handlePayment}
          style={{
            display: 'block',
            margin: '0 auto',
            padding: '15px 40px',
            backgroundColor: '#2E7D32',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '18px',
            fontWeight: 'bold',
            boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.2)',
            transition: 'all 0.3s ease-in-out',
          }}
          onMouseEnter={(e) => (e.target.style.backgroundColor = '#FF5C00')}
          onMouseLeave={(e) => (e.target.style.backgroundColor = '#2E7D32')}
        >
          Pay using Cash
        </button>
      </div>
    </div>
  );
};

export default CartPage;
