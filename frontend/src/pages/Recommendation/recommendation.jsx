import React, { useState } from 'react';
import './Recommendation.css'; // Import CSS for styling

function Recommendation() {
  const [dishName, setDishName] = useState('');
  const [userPreferences, setUserPreferences] = useState('Vegetarian');
  const [excludedIngredients, setExcludedIngredients] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [showModal, setShowModal] = useState(false);

  // Function to handle the form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const payload = {
      dish_name: dishName,
      user_preferences: userPreferences,
      excluded_ingredients: excludedIngredients
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setErrorMessage(errorData.message || 'An error occurred while fetching recommendations.');
      } else {
        const data = await response.json();
        setRecommendations(data);
        setErrorMessage('');
        setShowModal(false); // Close the modal after successful submission
      }
    } catch (error) {
      setErrorMessage('An error occurred while fetching recommendations.');
    }
  };

  return (
    <div className="recommendation-container">
      <h1>Dish Recommendation System</h1>

      {/* Button to open the modal */}
      <button className="toggle-button" onClick={() => setShowModal(true)}>
        Need Recommendations?
      </button>

      {/* Modal */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <span className="close-button" onClick={() => setShowModal(false)}>&times;</span>

            {/* Form inside the modal */}
            <form onSubmit={handleSubmit}>
              <label>
                Enter the dish you'd like to order:
                <input
                  type="text"
                  value={dishName}
                  onChange={(e) => setDishName(e.target.value)}
                />
              </label>
              <br />

              <label>
                Select your preference:
                <select
                  value={userPreferences}
                  onChange={(e) => setUserPreferences(e.target.value)}
                >
                  <option value="Vegetarian">Vegetarian</option>
                  <option value="NonVegetarian">Non-Vegetarian</option>
                </select>
              </label>
              <br />

              <label>
                Ingredients to exclude (comma-separated):
                <input
                  type="text"
                  value={excludedIngredients}
                  onChange={(e) => setExcludedIngredients(e.target.value)}
                />
              </label>
              <br />

              <button type="submit" className="submit-button">Get Recommendations</button>
            </form>

            {/* Error Message */}
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
          </div>
        </div>
      )}

      {/* Display recommendations */}
      {recommendations.length > 0 && (
        <div>
          <h2>Recommended Dishes:</h2>
          <table>
            <thead>
              <tr>
                <th>Dish Name</th>
                <th>Ingredients</th>
                <th>Rating</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              {recommendations.map((dish, index) => (
                <tr key={index}>
                  <td>{dish.Dish_Name}</td>
                  <td>{dish.Ingredients_List}</td>
                  <td>{dish.Dish_Rating}</td>
                  <td>{dish.Order_Price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Recommendation;
