import React, { useContext, useEffect, useState } from 'react'
import './Navbar.css'
// import { assets } from '../../assets/assets'
import { Link, useNavigate } from 'react-router-dom'
// import { StoreContext } from '../../Context/StoreContext'
import logo from '../../assets/logo.svg';
import { CgProfile } from "react-icons/cg";
import { TfiFacebook } from "react-icons/tfi";
import { FaXTwitter } from "react-icons/fa6";
import { FaInstagram } from "react-icons/fa";
import { FaOpencart } from "react-icons/fa";

const Navbar = ({ setShowLogin }) => {

  const [menu, setMenu] = useState("home");
  // const { getTotalCartAmount, token ,setToken } = useContext(StoreContext);
  // const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    // setToken("");
    // navigate('/')
  }

  return (
    <div className='navbar'>
      <img className='logo' src={logo} alt="" />
      <ul className="navbar-menu">
        {/* <Link to="/" onClick={() => setMenu("home")} className={`${menu === "home" ? "active" : ""}`}>home</Link> */}
        <a href='#explore-menu' onClick={() => setMenu("menu")} className={`${menu === "menu" ? "active" : ""}`}>menu</a>
        <a href='#app-download' onClick={() => setMenu("about")} className={`${menu === "about" ? "active" : ""}`}>about</a>
        <a href='#footer' onClick={() => setMenu("contact")} className={`${menu === "contact" ? "active" : ""}`}>contact us</a>
      </ul>
      <div className="navbar-right">
        {/* <img src={assets.search_icon} alt="" /> */}
        <FaOpencart size={22}/>
        {/* <Link to='/cart' className='navbar-search-icon'>
          <img src={assets.basket_icon} alt="" />
          <div className={getTotalCartAmount() > 0 ? "dot" : ""}></div>
        </Link> */}
        <button onClick={() => setShowLogin(true)}>sign in</button>
           <div className='navbar-profile'>
            <CgProfile/>
            <ul className='navbar-profile-dropdown'>
              <li onClick={()=>navigate('/myorders')}> <FaOpencart/> <p>Orders</p></li>
              <hr />
              {/* <li onClick={logout}> <img src={assets.logout_icon} alt="" /> <p>Logout</p></li>  */}
            </ul>
          </div>
        

      </div>
    </div>
  )
}

export default Navbar
