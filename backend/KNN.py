import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
import pickle
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('backend/dataset/optimisation_data.csv')

# Data Preprocessing
df['Dish_Rating'].fillna(df['Dish_Rating'].mean(), inplace=True)


label_encoder = LabelEncoder()
df['User_Preferences'] = label_encoder.fit_transform(df['User_Preferences'])
df['Season'] = label_encoder.fit_transform(df['Season'])


features = ['Dish_Rating']

df_encoded = pd.get_dummies(df[['Dish_Name','User_Preferences', 'Season','Ingredients_List']], drop_first=True) 
X = pd.concat([df[features], df_encoded], axis=1)    

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

df['Cluster'] = clusters

with open('kmeans_model.pkl', 'wb') as file:
    pickle.dump(kmeans, file)

df.to_csv('preprocessed_restaurant_data.csv', index=False)

print("Model and scaler saved as menu_optimization_model.pkl")