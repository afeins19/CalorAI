# generating the ml models 

# plotting (set matplot backend to not cause issues on mac idk why)
import matplotlib
matplotlib.use('Agg') # backend set 

from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns
from django.conf import settings 
import os
import re

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

# for getting the full path for the current OS
from pathlib import Path

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
def make_and_save_feature_importance_plots(x_label, y_label, model_name, file_path='mealGen/static/plot_images'):
    feature_importance = pd.DataFrame({'Feature': y_label, 'Importance': x_label})
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
    
    print(f"\nGenerating Plot for {model_name}...")
    # create the plot
    plt.figure(figsize=(12, 8))

    normalized_importances = feature_importance['Importance'] / feature_importance['Importance'].max()
    cmap = plt.get_cmap('viridis')
    colors = [cmap(i) for i in normalized_importances]

    sns.barplot(x='Importance', y='Feature', data=feature_importance, palette=colors)

    plt.title(f'Feature Importances for {model_name}')
    plt.xlabel('Importance')
    plt.ylabel('Features')

    # construct the full path with the base_dir
    file_name = model_name.lower() + "_feature_importance_plot.png"

    return save_plot_to_file(plot=plt, file_name=file_name)

def save_plot_to_file(plot, file_name, sub_folder='importance_plots'):
    plot_dir = Path(settings.BASE_DIR) / 'static' / sub_folder
    plot_dir.mkdir(parents=True, exist_ok=True) # make if folder isn't there

    file_path = plot_dir / file_name

    # saving the plot
    plot.savefig(file_path)
    plt.close()

    print(f"\nPlot Saved...\n")
    return file_path

def make_covariance_matrix(labels, data, model_name, file_path):
    cov_matrix = np.cov(data, rowvar=False) 

    # using seaborn to create the heatmap
    sns.set_theme(style="white")  
    plt.figure(figsize=(10, 8))  
    ax = sns.heatmap(cov_matrix, annot=True, fmt=".2f", cmap='coolwarm',
                     xticklabels=labels, yticklabels=labels,
                     cbar_kws={'label': 'Covariance'})
    plt.title('Covariance Matrix')
    plt.ylabel('Variables')
    plt.xlabel('Variables')
    
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # construct the full path with the base_dir
    file_name = model_name.lower() + "_cov_matrix.png"

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

# uses correlates from a given model to show instances that contributed most to exceeding calorie goal
# for now i will consider macro categories for features (carbs = breakfast_carbs + lunch_carbs + dinner_carbs, fat = breakfast_fat + ...)
def make_and_save_historical_data_plots(df: pd.DataFrame, top_correlates, plot_name, x_label=None, y_label=None, dates_goal_missed_cols=None, file_path='static/history_plots/', n_days=10):
    print(f"\nGetting Historical Examples from Correlates...")
    # n_days = number of days to display on the graph (10 by default unless df has less than 10 days)
    if n_days >= len(df):
        n_days=len(df)-1
    else:
        n_days -=1 # from 0 to n-1 days 

    # sorting the df by the calorie differnece (days with the highest)
    df_top_cal_diff_days = df.sort_values(by='calorie_diff', ascending=False)

    # converting date col to pd datetime and sorting by the date from the top 10
    df_top_cal_diff_days['date'] = pd.to_datetime(df_top_cal_diff_days['date']) 
    df_top_cal_diff_days_by_date = df_top_cal_diff_days.sort_values(by='date')

    # getting the top n_days 
    df_top_cal_diff_days = df_top_cal_diff_days[:n_days]
    print(f"TOP_10_BY_DATE:\n\n{df_top_cal_diff_days_by_date[:n_days]}\n\n")

    # for selecting macro cols
    f_types = ['fat', 'carbs', 'protein']
    # creating a string to match feature types with the randomly selected ones
    re_types = re.compile('|'.join(re.escape(f) for f in f_types))
    # searchable string of selected correlates
    corr_str = str("".join(top_correlates))

    # see which types the selected features fall under
    selected_macros = list(set(re_types.findall(corr_str)))
    print(f"Macro Types (will be summed daily)...{selected_macros}")

    df_macro_totals = pd.DataFrame(columns=[name+'_totals' for name in selected_macros]) # generating totals columns

    # add in date col if passed in
    if len(dates_goal_missed_cols) > 0:
        df_macro_totals['date'] = dates_goal_missed_cols

    # convert date col to datetime 
    df_macro_totals['date'] = pd.to_datetime(df_macro_totals['date'])

    for macro in selected_macros:
        # get all rows for the selected macro type
        df_macro_rows = df.filter(regex=macro+'$')
        # sum over each column and make a new data frame
        row_sums = df_macro_rows.sum(axis=1)

        df_macro_totals[macro+'_totals'] = row_sums

    # i think it woooooorks
    print(f"\n\n\n{df_macro_totals.head()}\n\n\n")

    # plot each line for each macro
    print("Generating Plots...")
    for macro in df_macro_totals.columns:
        plt.plot(df_macro_totals[macro], label=macro)
        print(f"\t[{macro} plotted...]")
    
    # setup plot
    if not x_label:
        x_label = 'Date'
    if not y_label:
        y_label = 'gr/day'

    file_path = file_path + plot_name + '_history_plot.png'

    fig, ax = plt.subplots(figsize=(20, 7))

    colors = ("orange", "skyblue", "limegreen")
    
    # pairs macro and color of its bar for display on graph
    for macro, color in zip(selected_macros, colors):
        ax.bar(df_macro_totals['date'], df_macro_totals[macro + '_totals'], label=macro, color=color)

    # formatting date on x-axis
    plt.tick_params(axis='x', which='major', labelsize='7')
    ax.xaxis.set_major_locator(mdates.DayLocator())  # tic for each day 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))  # date format 

    # make some rooooooooooom 
    plt.xticks(rotation=45)
    # plt.tight_layout()
   
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Macro Intake')
    ax.set_title('Daily Macro Intake on Days Calorie Goals Were Not Met')
    ax.legend()

    plt.show()

    # saving...
    print("saving plots...")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    plt.savefig(file_path)
    plt.close()

    return file_path

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