from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

with open('data_preprocessed.pkl', 'rb') as f:
    data = pickle.load(f)

def recommend_dishes(user_dish_name, user_preferences, excluded_ingredients):
    filtered_data = data[data['User_Preferences'].str.contains(user_preferences, case=False, na=False)]
    
    for ingredient in excluded_ingredients.split(","):
        filtered_data = filtered_data[~filtered_data['Ingredients_List'].str.contains(ingredient.strip(), case=False, na=False)]
    
    if filtered_data.empty:
        return "No dishes found that match your preferences and exclusions."
    
    filtered_data['Combined'] = filtered_data['Dish_Name'] + " " + filtered_data['Ingredients_List']
    
    if filtered_data['Combined'].str.strip().eq("").all():
        return "The resulting text data for TF-IDF is empty."
    
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(filtered_data['Combined'])
    except ValueError as e:
        return f"Error during TF-IDF vectorization: {e}"
    
    user_input_vector = vectorizer.transform([user_dish_name])
    cosine_similarities = cosine_similarity(user_input_vector, tfidf_matrix).flatten()
    
    filtered_data['Similarity'] = cosine_similarities
    filtered_data = filtered_data[filtered_data['Dish_Name'].str.lower() != user_dish_name.lower()]
    
    recommended_dishes = filtered_data.sort_values(by=['Similarity', 'Dish_Rating', 'Order_Price'], ascending=[False, False, True])
    
    unique_recommendations = recommended_dishes.drop_duplicates(subset='Dish_Name', keep='first').head(7)
    
    if unique_recommendations.empty:
        return "No recommendations found based on your input."
    
    # Return as a dictionary instead of DataFrame
    return unique_recommendations[['Dish_Name', 'Ingredients_List', 'Dish_Rating', 'Order_Price']].to_dict(orient="records")
