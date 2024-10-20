import React, { useState } from 'react';
import './optimisation.css';

function Optimisation() {
  const [isModalOpen, setModalOpen] = useState(false);
  const [trendingDishes, setTrendingDishes] = useState({ vegetarian: [], nonvegetarian: [] });
  const [error, setError] = useState(null);

  const fetchTrendingDishes = async () => {
    console.log("Fetching trending dishes..."); // Debugging log
    try {
      const response = await fetch('http://localhost:5000/trends');
      console.log("Response received: ", response); // Debugging log
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Data fetched: ", data); // Debugging log

      setTrendingDishes({
        vegetarian: data.vegetarian.slice(0, 3), // Display top 3 vegetarian dishes
        nonvegetarian: data.nonvegetarian.slice(0, 3), // Display top 3 non-vegetarian dishes
      });
      setModalOpen(true);
    } catch (error) {
      console.error("Error fetching trending dishes:", error);
      setError(error.message);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Discover What's Trending</h1>
      <button className="button" onClick={fetchTrendingDishes}>
        See What's in Trend
      </button>

      {error && <p className="error-message">Error: {error}</p>} {/* Show error if any */}

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2 className="modal-title">Trending Dishes</h2>

            <div className="dish-list">
              <h3>Vegetarian Dishes</h3>
              <ul>
                {trendingDishes.vegetarian.length === 0 ? (
                  <li>No dishes available</li>
                ) : (
                  trendingDishes.vegetarian.map((dish, index) => <li key={index}>{dish}</li>)
                )}
              </ul>

              <h3>Non-Vegetarian Dishes</h3>
              <ul>
                {trendingDishes.nonvegetarian.length === 0 ? (
                  <li>No dishes available</li>
                ) : (
                  trendingDishes.nonvegetarian.map((dish, index) => <li key={index}>{dish}</li>)
                )}
              </ul>
            </div>

            <button className="close-button" onClick={() => setModalOpen(false)}>
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Optimisation;
