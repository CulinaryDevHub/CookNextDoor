import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './Component/Navbar/Navbar.jsx'
import Header from './Component/Header/Header.jsx'
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
    </>
  )
}

export default App
