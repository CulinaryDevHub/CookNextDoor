import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { StoreContext } from '../context/StoreContext';
import { useNavigate } from 'react-router-dom';
import useAuthContext from '../context/AuthContext';

const Cart = () => {
    const { url, cartItems, setCartItems, quantity, setQuantity, getCustomerId, removeFromCart, getCartItems } = useContext(StoreContext) || {};
    // const [cartItems, setCartItems] = useState([]); // Initialize with an empty array
    const [errorMessage, setErrorMessage] = useState(""); // State to hold error messages, if any
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [user, setUser] = useState({ name: '', address: '', contact: '' });
    const [totalPrice, setTotal] = useState(0);
    const {token, loading} = useAuthContext()

    const headingStyle = {
        color: '#ffffff',
        width: '100%',
        textAlign: 'center',
        fontSize: '48px',
        marginBottom: '30px',
        fontFamily: "'Pacifico', cursive",
        backgroundColor: '#86c2b6', // Orange color for the heading
        padding: '15px 0',
        borderRadius: '10px',
        boxShadow: '0px 8px 15px rgba(0,0,0,0.1)',
    };

    const handlePayment = () => {
        navigate('/order-confirmation');
    };

    const handleEmailCheck = () => {
        fetch('http://localhost:5000/api/checkEmail', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    setErrorMessage(data.error);
                    setUser({ name: '', address: '', contact: '' });
                    setEmailVerified(false);
                } else {
                    setUser(data);
                    setErrorMessage('');
                    setEmailVerified(true);
                }
            })
            .catch((error) => console.error('Error checking email:', error));
    };

    // Function to fetch cart items
    const fetchCartItems = async () => {
        getCartItems();
    };

    useEffect(() => {
    if (!loading && token) {
      fetchCartItems();
    }
  }, [loading, token]);

    // Calculate total price whenever cartItems or quantity changes
    useEffect(() => {
        // Check if cartItems is an array
        if (Array.isArray(cartItems) && Array.isArray(quantity)) {
            const total = cartItems.reduce((acc, item, index) => {
                return acc + (item.price * (quantity[index] || 0)); // Ensure quantity[index] is not undefined
            }, 0);
            setTotal(total);
        } else {
            console.warn('cartItems or quantity is not an array:', { cartItems, quantity });
            setTotal(0); // Reset total if cartItems is not an array
        }
    }, [cartItems, quantity]);

    const incQuantity = (index) => {
        setQuantity(prevQuantity =>
            prevQuantity.map((qty, i) => i === index ? qty + 1 : qty) // Increment only the specific item
        );
        console.log(quantity);
    };
    const decQuantity = (index) => {
        setQuantity(prevQuantity =>
            prevQuantity.map((qty, i) => i === index ? (qty > 1 ? qty - 1 : 1) : qty)
        );
        console.log(quantity);
    };

    useEffect(() => {
        fetchCartItems();
        // console.log(cartItems);

    }, []);

    return (
        <div className='flex flex-col justify-center items-center'>
                <div>
                    {Array.isArray(cartItems) && cartItems.length === 0 ? (
                        <h1>Your cart is empty</h1>
                    ) : (
                        <div>
                            <div style={{ width: '80vw' }}>
                                <div className='flex bg-[#86C2B6] text-white px-6 py-4 text-lg font-bold'>
                                    <div className='pr-96 flex-1'>Order</div>
                                    <div className='flex-1'>Price (₹)</div>
                                    <div className='flex-1'>Quantity</div>
                                </div>
                            </div>

                            <ul>
                                {Array.isArray(cartItems) && cartItems.map((item, index) => (

                                    <li key={index} style={{ marginBottom: '20px', listStyle: 'none' }} className='flex gap-10 justify-between items-center my-2'>
                                        <div className='flex gap-2'>

                                            {item.image_url && (
                                                <img src={item.image_url} alt={item.dish_name} style={{ width: '200px' }} />
                                            )}
                                            <div className='w-96 mx-2 grid'>
                                                <h2 className='text-3xl font-medium'>{item.dish_name}</h2>
                                                <p>{item.description}</p>
                                                <p>{item.availability_status ? 'Available' : 'Out of Stock'}</p>
                                            </div>
                                        </div>
                                        <p>Price: ₹{item.price}</p>
                                        <div className='flex justify-center items-center'>
                                            <button onClick={() => decQuantity(index)} className='p-3 border-2'>-</button>
                                            <p className='p-3 border-y-2'>{quantity[index]}</p>
                                            <button onClick={() => incQuantity(index)} className='p-3 border-2'>+</button>
                                        </div>
                                        <button className='align-middle text-center w-28 h-12 bg-[#86c2b6] rounded-lg' onClick={() => removeFromCart(item.dish_id)}>Remove</button>
                                    </li>
                                ))}
                            </ul>
                            <div className='flex justify-center items-center text-3xl bg-gray-200 h-14'>
                                <h2>Total : ₹</h2>
                                <p>{totalPrice}</p>
                            </div>
                        </div>
                    )}
                </div>
            <button
                onClick={handlePayment}
                style={{
                    padding: '15px 25px',
                    backgroundColor: '#e76447', // Orange color for the button
                    color: '#fff',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '18px',
                    fontWeight: 'bold',
                    width: '50%',
                    boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.15)',
                    transition: 'background-color 0.3s ease, box-shadow 0.3s ease',
                    margin: '60px'
                }}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#E05C00'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FF5C00'}
            >
                Pay using Cash On Delivery
            </button>
    </div>
    )
};

export default Cart;
