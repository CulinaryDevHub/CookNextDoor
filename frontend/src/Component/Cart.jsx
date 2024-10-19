import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { StoreContext } from '../context/StoreContext';

const Cart = () => {
    const { url, cartItems, setCartItems, quantity, setQuantity, getCustomerId } = useContext(StoreContext) || {};
    // const [cartItems, setCartItems] = useState([]); // Initialize with an empty array
    const [errorMessage, setErrorMessage] = useState(""); // State to hold error messages, if any
    

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
            setCartItems(response.data.dish_details || []); // Store cart items in state, default to empty array if undefined
            // console.log(cartItems);
            
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

    const incQuantity = () =>{
        setQuantity(prevQuantity => prevQuantity + 1);
        console.log(quantity);
        
    }
    const decQuantity = () =>{
        setQuantity(prevQuantity => (prevQuantity > 1 ? prevQuantity - 1 : 1));
        console.log(quantity);
        
    }

    useEffect(() => {
        fetchCartItems();
        console.log(cartItems);
        
    }, []);

    return (
        <div>
            <h1 className='text-5xl font-semibold my-5 text-[#558177]'>Your Cart</h1>
            {errorMessage ? (
                <p style={{ color: 'red' }}>{errorMessage}</p>
            ) : (
                <div>
                    {Array.isArray(cartItems) && cartItems.length === 0 ? (
                        <h1>Your cart is empty</h1>
                    ) : (
                        <ul>
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
                                        <button onClick={decQuantity} className='p-3 border-2'>-</button>
                                        <p className='p-3 border-y-2'>{quantity}</p>
                                        <button onClick={incQuantity} className='p-3 border-2'>+</button>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    );
};

export default Cart;
