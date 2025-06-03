import React, { useState } from 'react'
// import Header from '../../components/Header/Header'
// import ExploreMenu from '../../components/ExploreMenu/ExploreMenu'
// import FoodDisplay from '../../components/FoodDisplay/FoodDisplay'
// import AppDownload from '../../components/AppDownload/AppDownload'
import Header from '../../Component/Header/Header'
import Menu from '../../Component/Menu/Menu'
import { StoreContextProvider } from '../../context/StoreContext'
import VendorList from '../../Component/VendorList'

const Home = () => {

  const [category,setCategory] = useState("All")

  return (
    <>
      <Header/>
      <StoreContextProvider>
        <VendorList/>
      </StoreContextProvider>
      {/* <ExploreMenu setCategory={setCategory} category={category}/>
      <FoodDisplay category={category}/>
      <AppDownload/> */}
    </>
  )
}

export default Home
