import React, { useState } from 'react'
// import Header from '../../components/Header/Header'
// import ExploreMenu from '../../components/ExploreMenu/ExploreMenu'
// import FoodDisplay from '../../components/FoodDisplay/FoodDisplay'
// import AppDownload from '../../components/AppDownload/AppDownload'
import Header from '../../Component/Header/Header'

const Home = () => {

  const [category,setCategory] = useState("All")

  return (
    <>
      <Header/>
      {/* <ExploreMenu setCategory={setCategory} category={category}/>
      <FoodDisplay category={category}/>
      <AppDownload/> */}
    </>
  )
}

export default Home
