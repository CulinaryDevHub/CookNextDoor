import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import React from 'react';
import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
import VendorDashboard from './Component/VendorDashboard.jsx';
import VendorDetails from './Component/VendorDetails.jsx';
import VendorList from './Component/VendorList.jsx';
import CustomerPage from './Component/CustomerPage.jsx';
import Recommendation from './pages/Recommendation/recommendation.jsx'
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
      <Recommendation/>
      {/* <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='/cart' element={<Cart />}/>
          <Route path='/order' element={<PlaceOrder />}/>
          <Route path='/myorders' element={<MyOrders />}/>
          <Route path='/verify' element={<Verify />}/>
      </Routes> */}
      <Router>
      <Routes>
        <Route path="/vendor/:vendorId" element={<VendorDetails />} />
        <Route path="/vendors" element={<VendorList />} />
        <Route path="/dashboard/:vendorId" element={<VendorDashboard />} />
        <Route path="/customer" element={<CustomerPage />} /> 
        <Route path="/" element={<VendorList />} />
      </Routes>
    </Router>
    </>
  )
}

export default App
