import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { StoreContext } from '../context/StoreContext';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
    const { url, cartItems, setCartItems, quantity, setQuantity, getCustomerId, removeFromCart } = useContext(StoreContext) || {};
    // const [cartItems, setCartItems] = useState([]); // Initialize with an empty array
    const [errorMessage, setErrorMessage] = useState(""); // State to hold error messages, if any
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [user, setUser] = useState({ name: '', address: '', contact: '' });
    const [totalPrice, setTotal] = useState(0);

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
        const customer_id = getCustomerId(); // Get customer ID
        if (!customer_id) {
            console.error('Customer ID not found. User may not be logged in.');
            setErrorMessage("Customer ID not found. User may not be logged in.");
            return; // Exit if customer_id is not available
        }

        try {
            const response = await axios.get(url + `/api/cart/${customer_id}`); // Fetch cart items
            const dishDetails = response.data.dish_details || [];  // Store cart items in state, default to empty array if undefined
            const details = dishDetails.map(item => item.details);  // Extract details if needed
            setCartItems(details);
            // console.log(cartItems);

            const dishQuantity = response.data.dish_details || [];  // Store cart items in state, default to empty array if undefined
            const fetchedquantity = dishQuantity.map(item => item.quantity);  // Extract details if needed
            setQuantity(fetchedquantity);

        } catch (error) {
            if (error.response) {
                console.error('Error response:', error.response.data);
                setErrorMessage(error.response.data.message || "Failed to fetch cart items");
            } else if (error.request) {
                console.error('Error request:', error.request);
                setErrorMessage("No response from the server");
            } else {
                console.error('Error message:', error.message);
                setErrorMessage(error.message);
            }
        }
    };

    // Calculate total price whenever cartItems or quantity changes
    useEffect(() => {
        // Check if cartItems is an array
        if (Array.isArray(cartItems) && Array.isArray(quantity)) {
            const total = cartItems.reduce((acc, item, index) => {
                return acc + (item.dish.price * (quantity[index] || 0)); // Ensure quantity[index] is not undefined
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
        console.log(cartItems);

    }, []);

    return (
        <div className='flex flex-col justify-center items-center'>
            {/* <h1 className='text-5xl font-semibold my-5 text-[#558177]'>Your Cart</h1> */}
            <h1 style={headingStyle}>
                🍽️ Customer's Cart 🛒
            </h1>
            <div style={{
                marginBottom: '30px',
                padding: '25px',
                border: '1px solid #ddd',
                borderRadius: '10px',
                backgroundColor: '#fff',
                boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.1)',
                transition: 'all 0.3s ease',
                textAlign: 'center',
                width: '100%'
            }}>
                <h2 style={{ color: '#006400', fontSize: '26px', marginBottom: '20px' }}>Enter Your Email</h2> {/* Dark green */}
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    style={{
                        padding: '12px',
                        fontSize: '18px',
                        width: '80%',
                        maxWidth: '450px',
                        marginBottom: '20px',
                        borderRadius: '5px',
                        border: '1px solid #ddd',
                        display: 'block',
                        marginLeft: 'auto',
                        marginRight: 'auto',
                        boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
                    }}
                />
                <button
                    onClick={handleEmailCheck}
                    style={{
                        padding: '12px 25px',
                        backgroundColor: '#e76447', // Orange color for the button
                        color: '#fff',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '18px',
                        fontWeight: 'bold',
                        boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.15)',
                        transition: 'background-color 0.3s ease, box-shadow 0.3s ease',
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#E05C00'}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#FF5C00'}
                >
                    Check Email
                </button>
                {errorMessage && <p style={{ color: 'red', marginTop: '10px' }}>{errorMessage}</p>}
            </div>
            {user.name && (
                <div style={{
                    marginBottom: '30px',
                    padding: '25px',
                    border: '1px solid #ddd',
                    borderRadius: '10px',
                    backgroundColor: '#fff',
                    boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.1)',
                    transition: 'all 0.3s ease',
                }}>
                    <h2 style={{ color: '#006400', fontSize: '26px', marginBottom: '20px', textAlign: 'center' }}>Customer Information</h2> {/* Dark green */}
                    <p style={{ fontSize: '18px' }}><strong>Name:</strong> {user.name}</p>
                    <p style={{ fontSize: '18px' }}><strong>Address:</strong> {user.address}</p>
                    <p style={{ fontSize: '18px' }}><strong>Contact:</strong> {user.contact}</p>
                </div>
            )}
            {errorMessage ? (
                <p style={{ color: 'red' }}>{errorMessage}</p>
            ) : (
                <div>
                    {Array.isArray(cartItems) && cartItems.length === 0 ? (
                        <h1>Your cart is empty</h1>
                    ) : (
                        <ul>
                            <table>
                                <thead>
                                    <tr style={{ backgroundColor: '#86C2B6', color: '#fff', display: 'flex', justifyContent: 'center', gap: '200px', width: '80vw' }}> {/* Dark green */}
                                        <th style={{ padding: '15px', border: 'none', fontSize: '18px', paddingRight: '200px' }}>Order</th>
                                        <th style={{ padding: '15px', border: 'none', fontSize: '18px' }}>Price (₹)</th>
                                        <th style={{ padding: '15px', border: 'none', fontSize: '18px' }}>Quantity</th>
                                    </tr>
                                </thead>
                            </table>
                            {Array.isArray(cartItems) && cartItems.map((item, index) => (
                                <li key={index} style={{ marginBottom: '20px', listStyle: 'none' }} className='flex gap-10 justify-between items-center my-2'>
                                    <div className='flex gap-2'>
                                        {/* {item.dish.image_url && ( */}
                                        <img src={item.dish.image_url} alt={item.dish.dish_name} style={{ width: '200px' }} />
                                        {/* )} */}
                                        <div className='w-96 mx-2 grid'>
                                            <h2 className='text-3xl font-medium'>{item.dish.dish_name}</h2>
                                            <p>{item.dish.description}</p>
                                            <p>{item.dish.availability_status ? 'Available' : 'Out of Stock'}</p>
                                        </div>
                                    </div>
                                    <p>Price: ₹{item.dish.price}</p>
                                    <div className='flex justify-center items-center'>
                                        <button onClick={() => decQuantity(index)} className='p-3 border-2'>-</button>
                                        <p className='p-3 border-y-2'>{quantity[index]}</p>
                                        <button onClick={() => incQuantity(index)} className='p-3 border-2'>+</button>
                                    </div>
                                    <button className='align-middle text-center w-28 h-12 bg-[#86c2b6] rounded-lg' onClick={() => removeFromCart(item.dish.dish_id)}>Remove</button>
                                </li>
                            ))}
                            <div className='flex justify-center items-center text-3xl bg-gray-200 h-14'>
                                <h2>Total : ₹</h2>
                                <p>{totalPrice}</p>
                            </div>
                        </ul>
                    )}
                </div>

            )}
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
    );
};

export default Cart;
