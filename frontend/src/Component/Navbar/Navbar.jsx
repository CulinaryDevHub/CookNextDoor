import React, { useContext, useEffect, useState } from 'react'
import './Navbar.css'
// import { assets } from '../../assets/assets'
import { Link, useNavigate } from 'react-router-dom'
import { StoreContext } from '../../context/StoreContext'
import logo from '../../assets/logo.svg';
import { CgProfile } from "react-icons/cg";
// import { TfiFacebook } from "react-icons/tfi";
// import { FaXTwitter } from "react-icons/fa6";
// import { FaInstagram } from "react-icons/fa";
import { FaOpencart } from "react-icons/fa";
import { jwtDecode } from 'jwt-decode';
import useAuthContext from '../../context/AuthContext';


const Navbar = ({ setShowLogin }) => {

  const [menu, setMenu] = useState("home");
  const { token, setToken } = useAuthContext()
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
    // navigate('/')
  }

  const getVendorIdFromToken = () => {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      return decodedToken.vendor_id; // Assuming user_id is the vendor_id
    }
    return null;
  };

  const handleDashboardClick = () => {
    const vendorId = getVendorIdFromToken();
    if (vendorId) {
      // Navigate to the dashboard with vendorId
      navigate(`/dashboard/${vendorId}`);
    } else {
      console.error('No vendor ID found or token is invalid.');
    }
  };

  return (
    <div className='navbar'>
      <img className='logo' src={logo} alt="" />
      <ul className="navbar-menu">
        <Link to="/" onClick={() => setMenu("home")} className={`${menu === "home" ? "active" : ""}`}>home</Link>
        <a href='/vendors' onClick={() => setMenu("menu")} className={`${menu === "menu" ? "active" : ""}`}>vendors</a>
        <a href='#app-download' onClick={() => setMenu("about")} className={`${menu === "about" ? "active" : ""}`}>about</a>
        <a href='#footer' onClick={() => setMenu("contact")} className={`${menu === "contact" ? "active" : ""}`}>contact us</a>
      </ul>
      <div className="navbar-right">
        {/* <img src={assets.search_icon} alt="" /> */}
        {/* <FaOpencart size={22}/> */}
        {/* <Link to='/cart' className='navbar-search-icon'>
          <img src={assets.basket_icon} alt="" />
          <div className={getTotalCartAmount() > 0 ? "dot" : ""}></div>
        </Link> */}
        {!token ? <button onClick={() => setShowLogin(true)}>sign in</button>
          : <div className='flex gap-10'><Link to='/cart' className='flex gap-3'> <FaOpencart size={20}/></Link>
          <div className='navbar-profile'>
            <CgProfile size={20}/>
            <ul className='navbar-profile-dropdown'>
              <li ><Link to='/cart' className='flex gap-3'><p>Orders</p></Link></li>
              <hr />
              <li onClick={logout}><p>Logout</p></li> 
              <hr />
              <li onClick={handleDashboardClick}><p>DashBoard</p></li>
            </ul>
          </div>
          </div>
        }

      </div>
    </div>
  )
}

export default Navbar
