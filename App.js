import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './gj.css';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Fetch initial processed ingredients and adulterants
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/process');
        setResult(response.data); // Set the result with data from the backend
      } catch (err) {
        setError('');
      }
    };

    fetchData();
  }, []); // Empty dependency array means this runs once when the component mounts

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    try {
      // Sending a POST request to Flask backend with the ingredients data
      const response = await axios.post('http://127.0.0.1:5000/process', { ingredients });
      setResult(response.data); // Update the result with the response data
      setError(null);           // Clear any previous error
    } catch (err) {
      setError('Error occurred while processing the request: ' + err.message);
      setResult(null);
    }
  };

  return (
    <div className="App">
      <h1>FoodGuard: Ingredient Fraud Detection System</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Enter Ingredients followed by spaces:
          <input
            type="text"
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
            placeholder="E.g., milk, sugar, honey"
            required
          />
        </label>
        <button type="submit">Check Ingredients</button>
      </form>

      {/* Display the result from backend */}
      {result && (
        <div>
          <h2>Processed Ingredients:</h2>
          <pre>{JSON.stringify(result.processed_ingredients, null, 2)}</pre>
          <h2>Detected Ingredients and Adulterants:</h2>
          <ul>
            {result['Ingredients detected'].map((ingredient, index) => (
              <li key={index}>
                <strong>{ingredient}</strong>: 
                {/* Check if the adulterants value is an array and join if true, otherwise display as it is */}
                {Array.isArray(result['Adulterants identified'][index])
                  ? result['Adulterants identified'][index].join(', ')
                  : result['Adulterants identified'][index] || 'None'}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Display an error message if there is an error */}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
