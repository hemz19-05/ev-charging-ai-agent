from flask import Flask, jsonify, request
import joblib
from preprocessing import preprocess_input


app = Flask(__name__)

model = joblib.load('ev_cost_model.pkl')


@app.route("/")
def home():
    return "🚗 EV Charging Prediction API is running!"


@app.route('/predict', methods=['POST'])
def predict():        
      
    try:
        
        data = request.get_json()

        X = preprocess_input(data)
        prediction = model.predict(X)[0]
        return jsonify({'prediction': float(prediction)})
    
    except Exception as e:
         return jsonify({'error': str(e)})




if __name__ == '__main__':
        app.run(debug=True)
