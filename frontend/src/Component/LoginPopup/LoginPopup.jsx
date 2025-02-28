import React, { useContext, useState, useEffect } from 'react'
import './LoginPopup.css'
// import { assets } from '../../assets/assets'
import axios from 'axios'
import { toast } from 'react-toastify'
import { StoreContext } from '../../context/StoreContext'

const LoginPopup = ({ setShowLogin }) => {

    const { setToken, url } = useContext(StoreContext) || {}
    // const [token, setToken] = useState("")
    const [currState, setCurrState] = useState("Login");
    // const url = "http://localhost:5000"

    const [data, setData] = useState({
        user_type: "",
        email: "",
        password: "",
        firstname: "",
        lastname: "",
        contact: "",
        address: "",
    })

    const onChangeHandler = (event) => {
        const name = event.target.name
        const value = event.target.value
        setData(data => ({ ...data, [name]: value }))
    }
    const onLogin = async (e) => {
        e.preventDefault()

        let new_url = url;
        if (currState === "Login") {
            new_url += "/api/user/logintoken";
        }
        else {
            new_url += "/api/user/addone"
        }

        try {
            const response = await axios.post(new_url, data, {
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            // Check for non-JSON responses, such as an HTML error page
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Invalid response format');
            }

            const result = response.data;
            console.log(result);
            

            if (result.success) {                
                setToken(result.token);
                localStorage.setItem("token", result.token);
                setShowLogin(false);
            } else {
                // toast.error(result.error || "Unauthorized");
                alert("Unauthorized")
            }
        } catch (error) {
            console.error('Error during login:', error);
            toast.error("An error occurred during Login");
        }
    }

    // const onLogin = async (e) => {
    //     e.preventDefault();

    //     let new_url = url;
    //     if (currState === "Login") {
    //         new_url += "/api/user/logintoken";
    //     } else {
    //         new_url += "/api/user/addone";
    //     }

    //     // Fetch options
    //     const options = {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(data),
    //     };

    //     try {
    //         const response = await fetch(new_url, options);

    //         // Check for non-JSON responses, such as an HTML error page
    //         const contentType = response.headers.get('content-type');
    //         if (!contentType || !contentType.includes('application/json')) {
    //             throw new Error('Invalid response format');
    //         }

    //         // // Log the raw response for debugging
    //         // const responseText = await response.text();
    //         // console.log('Raw response:', responseText);

    //         const result = await response.json();

    //         if (result.success) {
    //             setToken(result.token);
    //             localStorage.setItem("token", result.token);
    //             setShowLogin(false);
    //         } else {
    //             toast.error(result.message);
    //         }
    //     } catch (error) {
    //         console.error('Error during login:', error);
    //         toast.error("An error occurred during the request");
    //     }
    // };


    return (
        <div className='login-popup'>
            <form onSubmit={onLogin} className="login-popup-container">
                <div className="login-popup-title">
                    <h2>{currState}</h2> <img onClick={() => setShowLogin(false)} src={""/*assets.cross_icon*/} alt="" />
                </div>
                <div className="login-popup-inputs">
                    <input name='user_type' onChange={onChangeHandler} value={data.user_type} type="text" placeholder='Your role' required />
                    <input name='email' onChange={onChangeHandler} value={data.email} type="email" placeholder='Your email' />
                    <input name='password' onChange={onChangeHandler} value={data.password} type="password" placeholder='Password' required />
                    {currState === "Sign Up" ? <input name='firstname' onChange={onChangeHandler} value={data.firstname} type="text" placeholder='Your firstname' required /> : <></>}
                    {currState === "Sign Up" ? <input name='lastname' onChange={onChangeHandler} value={data.lastname} type="text" placeholder='Your lastname' required /> : <></>}
                    {currState === "Sign Up" ? <input name='contact' onChange={onChangeHandler} value={data.contact} type="text" placeholder='Your contact' required /> : <></>}
                    {currState === "Sign Up" ? <input name='address' onChange={onChangeHandler} value={data.address} type="text" placeholder='Your address' required /> : <></>}
                </div>
                <button>{currState === "Login" ? "Login" : "Create account"}</button>
                <div className="login-popup-condition">
                    <input type="checkbox" name="" id="" required />
                    <p>By continuing, i agree to the terms of use & privacy policy.</p>
                </div>
                {currState === "Login"
                    ? <p>Create a new account? <span onClick={() => setCurrState('Sign Up')}>Click here</span></p>
                    : <p>Already have an account? <span onClick={() => setCurrState('Login')}>Login here</span></p>
                }
            </form>
        </div>
    )
}

export default LoginPopup


// while loging in or signing up if want to go back to home page without loging in or signing up they cant do it
