import { useState } from 'react'


import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'

import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
import Footer from './Component/Footer/Footer.jsx'
import LoginPopup from './Component/LoginPopup/LoginPopup.jsx'
import Home from './pages/Home/Home.jsx'
import { StoreContextProvider } from './context/StoreContext.jsx'
import Cart from './Component/Cart.jsx'
import OrderConfirmation from './Component/OrderConfirmation'
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import VendorDetails from './Component/VendorDetails.jsx'
import Menu from './Component/Menu/Menu.jsx'
import VendorDashboard from './Component/VendorDashboard.jsx'
import VendorList from './Component/VendorList.jsx'
import { VendorContextProvider } from './context/VendorContext.jsx'
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
        <VendorContextProvider>
        <ToastContainer />
        {showLogin ? <LoginPopup setShowLogin={setShowLogin} /> : <></>}

        <div className='app'>
          <BrowserRouter>
            <Navbar setShowLogin={setShowLogin} />
            {/* <Navbar setShowLogin={setShowLogin}/> */}
            <Routes>
              <Route path='/' element={<Home />} />
              <Route path='/cart' element={<Cart />} />
              <Route path="/order-confirmation" element={<OrderConfirmation />} />
              <Route path="/vendor/:vendorId" element={<Menu />} />
              <Route path="/vendors" element={<VendorList />} />
              <Route path="/dashboard/:vendorId" element={<VendorDashboard />} />
              {/* <Route path='/order' element={<PlaceOrder />}/> */}
          {/* <Route path='/myorders' element={<MyOrders />}/> */}
          {/* <Route path='/verify' element={<Verify />}/> */}
            </Routes>
          </BrowserRouter>
        </div>
        <Footer />
        </VendorContextProvider>
      </StoreContextProvider>
    </>
  )
}

export default App
