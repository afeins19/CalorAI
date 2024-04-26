# generating the ml models 

# plotting (set matplot backend to not cause issues on mac idk why)
import matplotlib
matplotlib.use('Agg') # backend set 

import matplotlib.pyplot as plt 
import seaborn as sns
from django.conf import settings 
import os

# data handling
import pandas as pd 
from .preprocess import preprocess_data

# datasets for generic testing 
from sklearn.datasets import make_classification

# models 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler  
from sklearn.ensemble import RandomForestClassifier  
import xgboost as xgb 
from io import BytesIO
import base64
import numpy as np

def get_log_dates(df):
    return df['dates']

def have_same_shape(train, test):
    if train.shape[1] != test.shape[1]:
        print(f"[split_scale] INCONSISTENT X SHAPES: (Train:{train.shape}, Test:{test.shape})")
        return False
    return True 

def split_scale(df, target='calorie_diff'): 
    if df is not None and not df.empty:
        if target not in df.columns: 
            return None 
        
        # setting train and target 
        y = df[target]
        X = df.drop(target, axis=1)

        # stratify lets us balance training sets with balanced values of target variable 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        data = {"X_train_scaled" : X_train_scaled,
                "X_test_scaled" : X_test_scaled,
                "y_train" : y_train,
                "y_test" : y_test}
        
        print("\nData Split and Scaled...")

        # get shapes 
        print("DATA SHAPES: ")
        for partition, vals in data.items():
            print(partition, vals.shape)
        return data
    
    print("[split_scale] No Data Input")
    return None 

def train_random_forest(X_train, y_train):
    # training a random forest classifier 
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced') # balancing for good mix of calorie met vs unmet days 
    model.fit(X_train, y_train)
    print("Random Forest Model Trained...")
    return model 

def train_xgboost(X_train, y_train):
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    print("XGBoost Model Trained...")
    return model

def make_predictions(model, X_test):
    print(f"\nPredicting with {str(model)[:13]}...")
    predictions = model.predict(X_test)
    print(f"Predictions Made...")
    return predictions

def get_model_metrics(y_true, y_pred):
    # calculates model metrics 
    print(f"\nCalculating Model Metrics...")
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='macro')

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1}

# gets the most important features for the models predictions (sorted by importance)
def get_feature_importances(model, feature_names): 
    print(f"Getting Feature Importances for Model: {str(model)[:13]}")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_attrs = [(feature_names[i], importances[i]) for i in indices]
    return sorted_attrs

# makes and saves a horizontal bar plot 
def make_and_save_hbar_plot(x_label, y_label, model_name, file_path='mealGen/static/plot_images'):
    feature_importance = pd.DataFrame({'Feature': y_label, 'Importance': x_label})
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
    
    print(f"\nGenerating Plot for {model_name}...")
    # create the plot
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance)
    plt.title('Feature Importances')
    plt.xlabel('Importance')
    plt.ylabel('Features')
    
    # save the plot to a file
    plt.savefig(f"{model_name.lower()}_feature_importance_plot.png")
    plt.close()

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # construct the full path with the base_dir
    file_name = model_name.lower() + "_feature_importance_plot.png"

    full_path = os.path.join(settings.BASE_DIR, file_path, file_name)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    plt.savefig(full_path)
    print(f"Plot Saved...")
    return full_path

def to_base64(file_path):
    # gets b64 encoding of file 
    print(f"\nEncoding plot: {file_path}...")
    with open(file_path, 'rb') as f: 
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
    print("Plot Encoded...")
    return encoded_string

# testing with generic data 
if __name__ == "__main__":
    # Generate a synthetic dataset
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, random_state=42)
    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    df['target'] = y

    # Process the data
    processed_data = split_scale(df, 'target')
    if processed_data:
        # Train models
        rf_model = train_random_forest(processed_data['X_train_scaled'], processed_data['y_train'])
        xgb_model = train_xgboost(processed_data['X_train_scaled'], processed_data['y_train'])

        # Predict and evaluate
        rf_predictions = make_predictions(rf_model, processed_data['X_test_scaled'])
        xgb_predictions = make_predictions(xgb_model, processed_data['X_test_scaled'])

        rf_metrics = get_model_metrics(processed_data['y_test'], rf_predictions)
        xgb_metrics = get_model_metrics(processed_data['y_test'], xgb_predictions)

        print("Random Forest Metrics:", rf_metrics)
        print("XGBoost Metrics:", xgb_metrics)