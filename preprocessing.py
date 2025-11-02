import pandas as pd
import numpy as np
import joblib


FEATURES = joblib.load('model_features.pkl')
                       
def map_vehicle_model(model_name):
    known_models = ['Tesla Model 3', 'Hyundai Kona', 'Chevy Bolt', 'BMW i3', 'Nissan Leaf']
    
    if model_name in known_models:
        return model_name
    else:
        return 'BMW i3'  
    
def preprocess_input(data_dict):

    data_dict['Vehicle Model'] = map_vehicle_model(data_dict['Vehicle Model'])

    df = pd.DataFrame([data_dict])
    

    df['Battery Efficiency (km/kWh)'] = df['Distance Driven (since last charge) (km)'] / df['Energy Consumed (kWh)']
    df['Battery Efficiency (km/kWh)'] = df['Battery Efficiency (km/kWh)'].clip(upper=50)
    

    df = pd.get_dummies(df)

    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURES]
    
    return df



