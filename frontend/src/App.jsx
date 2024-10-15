import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
// import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
import Footer from './Component/Footer/Footer.jsx'
import LoginPopup from './Component/LoginPopup/LoginPopup.jsx'
import Home from './pages/Home/Home.jsx'
import { StoreContextProvider } from './context/StoreContext.jsx'
import CartPage from './Component/Cart/CartPage.jsx';
import OrderConfirmation from './Component/Cart/OrderConfirmation.jsx';

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
          <Routes>
            <Route path='/' element={<Home />} />
            {/* <Route path='/cart' element={<Cart />}/>
          <Route path='/order' element={<PlaceOrder />}/>
          <Route path='/myorders' element={<MyOrders />}/>
          <Route path='/verify' element={<Verify />}/> */}
          </Routes>
        </BrowserRouter>
      </div>
      {/* <Footer />
      <Navbar/>
      <Header/> */}
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<CartPage />} />
        <Route path="/order-confirmation" element={<OrderConfirmation />} />
        Add more routes as needed
      </Routes>
    </BrowserRouter>
    </>
  );
};


export default App 