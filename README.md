# CalorAI
given a users daily food-log data. This program will analyze trends between the data within a history of the user health logs and determine if there are any correlations between them and the user not meeting their desired health goals. 

 Structure
1. Core App

    Models: Common or base models.
    Utilities: Helper functions -> `/util`


2. ML App (e.g., data_analysis)

    ML Models: XGBoost, RandomForest
    Data Preprocessing: Custom Scripts in `/ml`
    Analysis: Core analysis and processing logic
    Result Storage: Models or methods for storing analysis results.

4. Data Processing App (e.g., data_processing) (Optional)

    Data Transformation: Code to transform raw data into a format suitable for ML analysis.
    Normalization: Functions to normalize or standardize data.

5. API App (e.g., api)

    Endpoints: API views or viewsets exposing data and functionalities.
    Serializers: Data serialization for API responses.
    Authentication and Permissions: API-specific auth and access control.

6. Frontend App (e.g., frontend) 

    Templates: Django templates for the frontend.
    Static Files: CSS, JavaScript, and other static files.

