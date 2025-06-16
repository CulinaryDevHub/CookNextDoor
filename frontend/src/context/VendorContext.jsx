import { createContext, useContext } from "react";

const VendorContext = createContext({})

export const VendorContextProvider = VendorContext.Provider

export default function useVendorContext(){
    return useContext(VendorContext)
}