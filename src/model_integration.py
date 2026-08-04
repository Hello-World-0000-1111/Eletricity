import os
import pickle
import numpy as np
import pandas as pd
import datetime

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'xgboost.pkl')

# Load the model
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

def prepare_features(user_input):
    """
    Prepares the feature array based on user input.
    Expected features by model:
    date, city, temperature_c, humidity_percent, electricity_units_kwh, household_size,
    income_level, power_outage_hours, year, month, day, day_of_week, is_weekend,
    lag_1, lag_7, lag_30, rolling_mean_7, rolling_mean_30
    
    Since we are predicting electricity_units_kwh, it shouldn't be in the input features
    unless it was in the training data by mistake. Let's assume the model uses:
    city, temperature_c, humidity_percent, household_size, income_level, power_outage_hours,
    year, month, day, day_of_week, is_weekend, lag_1, lag_7, lag_30, rolling_mean_7, rolling_mean_30
    """
    now = datetime.datetime.now()
    
    # Defaults or mocked values for lag and rolling means to allow the demo to work
    # In a production setting, these would be fetched from the database
    feature_dict = {
        'city': user_input.get('city', 0),
        'temperature_c': user_input.get('temperature_c', 25.0),
        'humidity_percent': user_input.get('humidity_percent', 50),
        'household_size': user_input.get('household_size', 4),
        'income_level': user_input.get('income_level', 1),
        'power_outage_hours': user_input.get('power_outage_hours', 0.0),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'day_of_week': now.weekday(),
        'is_weekend': 1 if now.weekday() >= 5 else 0,
        'lag_1': 20.0,
        'lag_7': 20.0,
        'lag_30': 20.0,
        'rolling_mean_7': 20.0,
        'rolling_mean_30': 20.0
    }
    
    # Convert to DataFrame to ensure correct column names and order if model is a pipeline/pandas based
    df = pd.DataFrame([feature_dict])
    return df

def predict_electricity(user_input):
    """
    Generates a prediction using the loaded model.
    """
    if model is None:
        # Fallback dummy prediction if model is not found
        return round(20.0 + user_input.get('temperature_c', 25) * 0.5, 2)
    
    try:
        features = prepare_features(user_input)
        prediction = model.predict(features)
        
        if isinstance(prediction, (np.ndarray, list)):
            return round(float(prediction[0]), 2)
        return round(float(prediction), 2)
    except Exception as e:
        print(f"Prediction error: {e}")
        # Fallback dummy prediction
        return round(20.0 + user_input.get('temperature_c', 25) * 0.5, 2)
