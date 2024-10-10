import React from 'react';

const OrderConfirmation = () => {
  return (
    <div style={{ 
      padding: '40px', 
      textAlign: 'center', 
      fontFamily: "'Poppins', sans-serif", 
      backgroundColor: '#fff', 
      borderRadius: '12px', 
      boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)', 
      margin: '50px auto', 
      maxWidth: '500px' 
    }}>
      <h2 style={{ 
        color: '#FF5C00', 
        fontSize: '32px', 
        marginBottom: '20px', 
        background: '#FFF',
        WebkitBackgroundClip: 'text',
        color: '#FF5C00',
      }}>Order Confirmed!</h2>
      <p style={{ 
        fontSize: '20px', 
        color: '#333', 
        marginBottom: '15px' 
      }}>Your order has been successfully placed.</p>
      <p style={{ 
        fontSize: '18px', 
        color: '#555', 
        marginBottom: '30px' 
      }}>Thank you for choosing us! We appreciate your business.</p>
      <p style={{ 
        fontSize: '16px', 
        color: '#777' 
      }}>You will receive a confirmation email shortly.</p>
      
      {/* Button to go back to Home */}
      <button 
        style={{ 
          marginTop: '30px', 
          padding: '12px 30px', 
          backgroundColor: '#2E7D32', 
          color: '#fff', 
          border: 'none', 
          borderRadius: '8px', 
          fontSize: '16px', 
          cursor: 'pointer', 
          fontWeight: 'bold',
          boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s ease-in-out' 
        }}
        onMouseEnter={(e) => (e.target.style.backgroundColor = '#FF5C00')}
        onMouseLeave={(e) => (e.target.style.backgroundColor = '#2E7D32')}
      >
        Back to Home 
      </button>
    </div>
  );
};

export default OrderConfirmation;
