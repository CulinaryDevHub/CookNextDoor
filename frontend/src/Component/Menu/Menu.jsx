import {React, useContext} from 'react'
import { StoreContext } from '../../context/StoreContext';

const Menu = () => {

    const { food_list, url, cartItems, setCartItems, addToCart } = useContext(StoreContext) || {};
    // console.log(food_list);
    
    // const handleAddToCart = async (dish_id) => {
    //     const token = localStorage.getItem('token');
    //     try {
    //         const response = await axios.post(
    //             `${url}/api/cart/add`,
    //             { dish_id },  // Sending the dish ID in the body
    //             { headers: { Authorization: `Bearer ${token}` } } // Include token for authentication
    //         );
    //         console.log('Add to cart response:', response.data);
    //     } catch (error) {
    //         console.error('Error adding to cart:', error);
    //     }
    // };

    return (
        <div className='my-10' id='food-display'>
            <h2 className='text-5xl m-5 font-bold'>Top dishes near you</h2>
            <div className='flex gap-12'>
            {Array.isArray(food_list) && food_list.length > 0 ? (
                    food_list.map((item) => (
                        <div className='w-96 grid gap-1' key={item.dish_id}>
                            <img
                                src={item.image_url || 'default-image-url.jpg'} // Default image if none is provided
                                alt={item.dish_name}
                                className='size-28'
                            />
                            <h3 className='text-2xl font-semibold'>{item.dish_name}</h3>
                            <p className='food-item-description'>{item.description}</p>
                            <p className='food-item-ingredients'>{item.ingredients}</p>
                            <p className='font-semibold text-lg'>₹{item.price}</p>
                            <p className='food-item-availability'>
                                {item.availability_status ? 'Available' : 'Not Available'}
                            </p>
                            <button className='align-middle text-center w-28 h-12 bg-[#86c2b6]' onClick={() => addToCart(item.dish_id)}>Add to Cart</button>
                        </div>
                    ))
                ) : (
                    <p>No dishes available or loading...</p> // Fallback message if food_list is empty or undefined
                )}
            </div>
        </div>
    )
}

export default Menu