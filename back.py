from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import spacy

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the CSV file into a pandas DataFrame
adulterated_ingredients_df = pd.read_csv('adulterated_ingredients_dataset.csv')

# Load the spaCy model for NLP processing
nlp = spacy.load('en_core_web_sm')

# Function to detect adulterants based on the CSV file
def detect_adulterants(ingredients):
    # Get the list of known adulterants
    ingredients_list = adulterated_ingredients_df['Ingredient Group'].str.lower().tolist()
    
    detected_ing = []
    adulterants_detected = []  # Initialize the list for detected adulterants
    for ingredient in ingredients:
        # Normalize ingredient for comparison
        ingredient = ingredient.strip().lower()
        # Check if the ingredient is in the list of known adulterants
        if ingredient in ingredients_list:
            detected_ing.append(ingredient)

            # Find the index of the matched ingredient in the DataFrame
            index = adulterated_ingredients_df[adulterated_ingredients_df['Ingredient Group'].str.lower() == ingredient].index.tolist()

            # Check if index is not empty
            if index:
                # Access the row using the first index found
                matched_row = adulterated_ingredients_df.iloc[index[0]]
                # Get corresponding adulterants and extend the list
                adulterants_detected.append(matched_row['Adulterants'].split(','))  # Assuming adulterants are comma-separated

    return detected_ing, adulterants_detected

# Function to process ingredients using NLP
def process_nlp(ingredients):
    # Use spaCy to create a document object
    doc = nlp(ingredients)
    # Extract and return unique ingredient terms from the document
    ingredients_list = set()
    for token in doc:
        # Consider only noun-like terms (you can refine this as needed)
        if token.pos_ in ['NOUN']:
            ingredients_list.add(token.text.strip().lower())
    return list(ingredients_list)

# Define the /process endpoint for POST requests
@app.route('/process', methods=['POST'])
def process():
    data = request.json  # Get JSON data from the frontend
    ingredients_input = data.get('ingredients', '')  # Extract the ingredients from the request

    # Ensure input is not empty
    if not ingredients_input:
        return jsonify({"error": "No ingredients provided."}), 400
    
    # Process NLP to extract entities (ingredients)
    processed_ingredients = process_nlp(ingredients_input)
    
    # Detect adulterants from the CSV
    detected_ing, adulterants = detect_adulterants(processed_ingredients)

    # Return the results as JSON
    return jsonify({
        "processed_ingredients": processed_ingredients,
        "Ingredients detected": detected_ing,
        "Adulterants identified": adulterants
    })

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
