import joblib

features = joblib.load('model_features.pkl')

vehicle_features = [f for f in features if 'Vehicle Model_' in f]
print(vehicle_features)
