import pandas as pd
import pickle
import re

file_path = r'C:\Users\sahuj\Desktop\mp-main\CookNextDoor\backend\dataset\restaurant_data.csv'
data = pd.read_csv(file_path)


def clean_text(text):
  
    text = text.lower()
    
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
   
    text = re.sub(r'\s+', ' ', text).strip()
    return text


data['User_Preferences'] = data['User_Preferences'].fillna('').apply(lambda x: clean_text(x) if isinstance(x, str) else x)
data['Ingredients_List'] = data['Ingredients_List'].fillna('').apply(lambda x: clean_text(x) if isinstance(x, str) else x)
data['Dish_Name'] = data['Dish_Name'].fillna('').apply(lambda x: clean_text(x) if isinstance(x, str) else x)

data['Dish_Rating'] = data['Dish_Rating'].fillna(0)
data['Order_Price'] = data['Order_Price'].fillna(0)

with open('data_preprocessed.pkl', 'wb') as f:
    pickle.dump(data, f)

