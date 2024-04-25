# CalorAI
given a users daily food-log data. This program will analyze trends between the data within a history of the user health logs and determine if there are any correlations between them and the user not meeting their desired health goals.
### Target Variable 
The target variable which our model will predict is the users's total daily caloric intake. 

### Features 
the model will gather the following data from the user's MyFitnessPal account and will then process it for use in the model. We will be using the following features to train the model:

- Food Type (fruit, vegetable, grain, protein. other)
- Calorie Percentage of Meal Type Out of Daily Calorie Count 
- Average Time Between Meals (on a given day)
- Time of day that meals are consumed (in hourly increments)
- Macro-nutrients (protein, carbs, fat)

 Structure
1. Core App

    Models: Common or base models.
    Utilities: Helper functions and utilities used across the project.
    Middleware: Common middleware, such as for logging or user authentication.

2. ML App (e.g., data_analysis)

    ML Models: scikit-learn -> XGBoost & RandomForest
    Data Preprocessing: Scripts or functions for data cleaning and preparation.
    Analysis: Core analysis and processing logic.


3. Scaling and Preprocessing
    - Standard Scaler
    - balanced_classes (Random Forest)

4. Frontend App (e.g., frontend) 

    Templates: Django templates for the frontend.
    Static Files: CSS, html
