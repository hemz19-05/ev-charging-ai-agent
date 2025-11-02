import os
import psycopg2
import pandas as pd
import joblib
from openai import OpenAI
from preprocessing import preprocess_input
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def connect_db():
    engine = create_engine("postgresql+psycopg2://postgres:Hzz19!#%@localhost:5432/ev_charging_db")
    return engine


model = joblib.load('ev_cost_model.pkl')
features = joblib.load('model_features.pkl')

def ai_agent_query(user_input):
     engine = connect_db()
     query_result = ''

     with engine.connect() as conn:
          if 'average' in user_input.lower() or 'total' in user_input.lower():
               df = pd.read_sql_query('SELECT * FROM ev_predictions;', conn)
               query_result = f"Data summary:\nAverage cost: {df['predicted_cost'].mean():.2f}\nTotal sessions: {len(df)}"
          elif 'predict' in user_input.lower():
               example_data = {
                    'Battery Capacity (kWh)': 50,
                    'Charging Duration (hours)': 2,
                    'Charging Rate (kW)': 11,
                    'State of Charge (Start %)': 30,
                    'State of Charge (End %)': 90,
                    'Temperature (°C)': 25,
                    'Vehicle Age (years)': 3,
                    'Vehicle Model': 'Tesla Model 3',
                    'Charger Type': 'Level 2',
                    'User Type': 'Commuter',
                    'Distance Driven (since last charge) (km)': 150,
                    'Energy Consumed (kWh)': 30
               }

               X = preprocess_input(example_data)
               prediction = model.predict(X)[0]
               query_result = f'Predicted charging cost: ${prediction:.2f}'


     response = client.chat.completions.create(
          model = 'gpt-4o-mini',
          messages = [
               {'role':'system', 'content': 'You are an EV charging assistant. Respond in a friendly and helpful tone.'},
               {'role':'user', 'content': f'User asked: {user_input}\nData retrieved: {query_result}'}
          ]
     )

     return response.choices[0].message.content


if __name__ == '__main__':
     print('⚡ EV Charging AI Assistant Ready! Type "exit" to quit.\n')
     while True:
          user_input = input('You: ')
          if user_input.lower() in ['exit', 'quit']:
               print('Goodbye!')
               break
          reply = ai_agent_query(user_input)
          print(f'🤖 Agent: {reply}\n')

