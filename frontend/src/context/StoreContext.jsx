import { Children, createContext, useEffect, useState } from "react";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import useAuthContext from "./AuthContext";


const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
    const {token, setToken} = useAuthContext()
    const url = "http://localhost:5000"
    const [food_list, setFoodList] = useState([]);
    const [cartItems, setCartItems] = useState({});
    // const [token, setToken] = useState("")
    const [quantity, setQuantity] = useState(1)

    // console.log(token);
    // Function to get customer ID from the token
    const getCustomerId = () => {
        // const token = localStorage.getItem('token'); // Get token from localStorage
        if (token) {
            setToken(token);
            
            try {
                const decoded = jwtDecode(token); // Decode the token
                // console.log(decoded.sub);

                return decoded.sub; // Return customer_id from the decoded token
            } catch (error) {
                console.error('Token decoding failed:', error);
                return null; // Handle case where decoding fails
            }
        }
        return null; // Handle case where token is not available
    };

    const getCartItems = async () => {
        const customer_id = getCustomerId(); // Get customer ID
        if (!customer_id) {
            console.error('Customer ID not found. User may not be logged in.');
            return; // Exit if customer_id is not available
        }
        
        // if (token && customer_id) {
            try {
                const response = await axios.get(
                    url + `/api/cart`,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    }
                ); // Fetch cart items
                const dishDetails = response.data.dish_details || [];  // Store cart items in state, default to empty array if undefined
                console.log(dishDetails);

                const details = dishDetails.map(item => item.details);  // Extract details if needed
                setCartItems(details);

                const dishQuantity = response.data.dish_details || [];  // Store cart items in state, default to empty array if undefined
                const fetchedquantity = dishQuantity.map(item => item.quantity);  // Extract details if needed
                setQuantity(fetchedquantity);

            } catch (error) {
                if (error.response) {
                    console.error('Error response:', error.response.data);
                    // setErrorMessage(error.response.data.message || "Failed to fetch cart items");
                } else if (error.request) {
                    console.error('Error request:', error.request);
                    // setErrorMessage("No response from the server");
                } else {
                    console.error('Error message:', error.message);
                    // setErrorMessage(error.message);
                }
            }
        // }
    }

    const addToCart = async (dish_id) => {
        const customer_id = getCustomerId()

        console.log("Adding to cart:", dish_id);
        // Update the cart items in the frontend state
        if (!cartItems[dish_id]) {
            setCartItems((prev) => ({ ...prev, [dish_id]: 1 }));
        } else {
            setCartItems((prev) => ({ ...prev, [dish_id]: prev[dish_id] + 1 }));
        }
        // console.log("after if");

        // If there's a token, send the cart update request to the backend
        if (token && customer_id) {
            try {
                await axios.post(
                    url + "/api/cart/add",
                    { dish_id },  // Send the dish_id in the request body
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    }  // Set Authorization header
                );
                console.log(`Dish ${dish_id} added to cart`);
                alert('dish added!')
            } catch (error) {
                if (error.response) {
                    console.error('Error adding dish to cart r:', error.response.data); // Log server's error message
                } else {
                    console.error('Error adding dish to cart:', error);
                }
            }

        } else {
            console.log('No token found. Please login.');
        }
    };

    function refreshPage() {
        window.location.reload(false); // Reload the page from the cache
    }

    const removeFromCart = async (dish_id) => {
        const customer_id = getCustomerId()

        console.log("Adding to cart:", dish_id);
        // Update the cart items in the frontend state
        if (!cartItems[dish_id]) {
            setCartItems((prev) => ({ ...prev, [dish_id]: 1 }));
        } else {
            setCartItems((prev) => ({ ...prev, [itemId]: prev[itemId] - 1 }))
        }
        // console.log("after if");

        if (token && customer_id) {
            try {
                await axios.delete(
                    url + "/api/cart/remove",
                    {  // Third argument for Axios includes the headers and the data
                        headers: {
                            "Authorization": `Bearer ${token}`,  // Assuming you're using Bearer token auth
                            "Content-Type": "application/json"  // Ensure the correct Content-Type is set
                        },
                        data: {  // The request body (data) goes here
                            dish_id: dish_id,
                            customer_id: customer_id
                        }
                    }
                );
                console.log(`Dish ${dish_id} deleted from cart`);
                alert('dish deleted!')
                refreshPage();
            } catch (error) {
                if (error.response) {
                    console.error('Error deleting dish to cart:', error.response.data); // Log server's error message
                } else {
                    console.error('Error deleting dish to cart:', error);
                }
            }

        } else {
            console.log('No token found. Please login.');
        }
    }

    const fetchMenu = async () => {
        try {
            const response = await axios.get(url + "/api/vendors");
            setFoodList(response.data.dishes); // Make sure you use the right key from the response
        } catch (error) {
            console.error('Error fetching food list:', error);
        }
    }

    useEffect(() => {
        async function loadData() {
            await fetchMenu();
            if (localStorage.getItem("token")) {
                // setToken(localStorage.getItem("token"))
                // await loadCartData({ token: localStorage.getItem("token") })
                // console.log(localStorage.getItem("token"));
            }
        }
        
        loadData()
    }, [token])

    useEffect(() => {
        // console.log(token);
        
    },[])

    const contextValue = {
        url,
        food_list,
        quantity,
        setQuantity,
        // menu_list,
        cartItems,
        addToCart,
        getCustomerId,
        removeFromCart,
        // getTotalCartAmount,
        token,
        setToken,
        // loadCartData,
        setCartItems,
        getCartItems
    };

    return (
        <StoreContext.Provider value={contextValue}>
            {props.children}
        </StoreContext.Provider>
    )
}

export { StoreContextProvider, StoreContext };
