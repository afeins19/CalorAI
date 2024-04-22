# generating the ml models 

# data handling
import pandas as pd 
from .preprocess import preprocess_data

# models 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
from sklearn.preprocessing import StandardScaler 
import xgboost as xgb 

# plots
import matplotlib as plt 
import seaborn as sns

def split_scale(df): 
    if df is not None and not df.empty:
        y = df['calorie_diff']
        X = df.drop('calorie_diff', axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        data = {"x_train_scaled" : X_train_scaled,
                "x_test_scaled" : X_test,
                "y_train" : y_train,
                "y_test" : y_test}
        
        print("Data Split and Scaled...")
        return data
    
    print("[split_scale()] No Data Input")
    return None 