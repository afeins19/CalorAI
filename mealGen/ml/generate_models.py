# generating the ml models 

# data handling
import pandas as pd 
from ml.preprocess import preprocess_data

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

def split_scale(df, target='caolrie_diff'): 
    if df is not None and not df.empty:
        if target not in df.columns: 
            return None 
        
        y = df[target]
        X = df.drop(target, axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        data = {"X_train_scaled" : X_train_scaled,
                "X_test_scaled" : X_test_scaled,
                "y_train" : y_train,
                "y_test" : y_test}
        
        print("Data Split and Scaled...")
        return data
    
    print("[split_scale] No Data Input")
    return None 

def train_random_forest(X_train, y_train):
    # training a random forest classifier 
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Random Forest Model Trained...")
    return model 

def train_xgboost(X_train, y_train):
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    print("XGBoost Model Trained...")
    return model

def make_predictions(model, X_test):
    predictions = model.predict(X_test)
    print(f"Predictions Made...")
    return predictions

def get_model_metrics(y_true, y_pred):
    # calculates model metrics 
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

# gets the most important features for the models predictions 
def get_feature_importances(model, feature_names): 
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_names = [feature_names[i] for i in indices]
    return sorted_names

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