import { useState } from 'react'

// import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
// import React from 'react';
import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
import Footer from './Component/Footer/Footer.jsx'
import LoginPopup from './Component/LoginPopup/LoginPopup.jsx'
import Home from './pages/Home/Home.jsx'
import { StoreContextProvider } from './context/StoreContext.jsx'
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
  const [showLogin, setShowLogin] = useState(false)

  return (
    <>
    <StoreContextProvider>
      {showLogin ? <LoginPopup setShowLogin={setShowLogin} /> : <></>}
      </StoreContextProvider>
      <div className='app'>
      
        <BrowserRouter>
          <StoreContextProvider>
            <Navbar setShowLogin={setShowLogin} />
          </StoreContextProvider>
          {/* <Navbar setShowLogin={setShowLogin}/> */}
          {/* <Header /> */}
          <Recommendation/>
          <Routes>
            <Route path='/' element={<Home />} />
            
            {/* <Route path='/cart' element={<Cart />}/>
      <Navbar/>
      <Header/>
      <Recommendation/>
      {/* <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='/cart' element={<Cart />}/>
          <Route path='/order' element={<PlaceOrder />}/>
          <Route path='/myorders' element={<MyOrders />}/>
          <Route path='/verify' element={<Verify />}/> */}

          <Route path="/vendor/:vendorId" element={<VendorDetails />} />
        <Route path="/vendors" element={<VendorList />} />
        <Route path="/dashboard/:vendorId" element={<VendorDashboard />} />
        <Route path="/customer" element={<CustomerPage />} /> 
        {/* <Route path='/verify' element  ={<Verify />}/> */}

        {/* <Route path="/" element={<VendorList />} /> */}
          </Routes>
        </BrowserRouter>
      </div>
      <Footer />
          
        {/* </Routes> */}

      
    </>
  )
}

export default App
