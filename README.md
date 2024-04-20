# OptimumMealGenerator
given a users MyFitnesspal data. This program will apply machine learning to a users eating habits and food choices to try to predict calorie intake based on those metrics. This will allow the model to inform the user about which of his or her particular dietary habits contribute most to his or her daily calorie goals. 

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

2. MyFitnessPal Integration App (e.g., fitness_data)

    API Connectors: Modules for connecting to the MyFitnessPal API.
    Data Downloaders: Functions or classes that handle downloading data in CSV format.
    Auth: Authentication mechanisms with MyFitnessPal.
    Management Commands: For tasks like periodic data syncing.

3. ML App (e.g., data_analysis)

    ML Models: Machine learning models, possibly using frameworks like scikit-learn, TensorFlow, or PyTorch.
    Data Preprocessing: Scripts or functions for data cleaning and preparation.
    Analysis: Core analysis and processing logic.
    Result Storage: Models or methods for storing analysis results.

4. Data Processing App (e.g., data_processing) (Optional)

    Data Transformation: Code to transform raw data into a format suitable for ML analysis.
    Normalization: Functions to normalize or standardize data.

5. API App (e.g., api)

    Endpoints: API views or viewsets exposing data and functionalities.
    Serializers: Data serialization for API responses.
    Authentication and Permissions: API-specific auth and access control.

6. Frontend App (e.g., frontend) (If not using a SPA framework)

    Templates: Django templates for the frontend.
    Static Files: CSS, JavaScript, and other static files.