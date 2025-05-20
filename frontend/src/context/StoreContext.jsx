import { Children, createContext, useEffect, useState } from "react";
import axios from "axios";
const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
    const url = "http://localhost:5000"
    const [food_list, setFoodList] = useState([]);
    const [cartItems, setCartItems] = useState({});
    const [token, setToken] = useState("")

    useEffect(() => {
        function loadData() {
            if (localStorage.getItem("token")) {
                setToken(localStorage.getItem("token"))
                // await loadCartData({ token: localStorage.getItem("token") })
                console.log(token);
            }
        }
        loadData()
    }, [token])

    const contextValue = {
        url,
        // food_list,
        // menu_list,
        // cartItems,
        // addToCart,
        // removeFromCart,
        // getTotalCartAmount,
        token,
        setToken
        // loadCartData,
        // setCartItems
    };

    return (
        <StoreContext.Provider value={contextValue}>
            {props.children}
        </StoreContext.Provider>
    )
}

export { StoreContextProvider, StoreContext };
