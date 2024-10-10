import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CartPage from './Component/Cart/CartPage.jsx';
import OrderConfirmation from './Component/Cart/OrderConfirmation.jsx';

// import Home from './pages/Home/Home.jsx'
// import Cart from './pages/Cart/Cart.jsx'
// import PlaceOrder from './pages/PlaceOrder/PlaceOrder.jsx'
// import MyOrders from './pages/MyOrder/MyOrders.jsx'
// import Verify from './pages/Verify/Verify.jsx'

function App() {
  return (
    <>
      <Navbar/>
      <Header/>
      {<Router>
      <Routes>
        <Route path="/" element={<CartPage />} />
        <Route path="/order-confirmation" element={<OrderConfirmation />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>}
    </>
  );
};


export default App
