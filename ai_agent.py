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
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("⚠️ DATABASE_URL not found in environment variables.")
        return None
    
    engine = create_engine(database_url)
    return engine

model = joblib.load('ev_cost_model.pkl')
features = joblib.load('model_features.pkl')

# Conversation history
conversation_history = []

def ai_agent_query(user_input):
    query_result = ''
    
    try:
        engine = connect_db()
        
        with engine.connect() as conn:
            if 'average' in user_input.lower() or 'total' in user_input.lower():
                df = pd.read_sql_query('SELECT * FROM ev_predictions;', conn)
                if not df.empty:
                    query_result = f"Data summary:\nAverage cost: ${df['predicted_cost'].mean():.2f}\nTotal sessions: {len(df)}"
                else:
                    query_result = "No predictions stored in database yet."
                    
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
                energy = example_data['Energy Consumed (kWh)']

                
                prediction_per_kwh = model.predict(X)[0]  # cost per kWh
                total_cost = prediction_per_kwh * energy  # total = rate × energy consumed
                query_result = (
                        f"Predicted rate: ${prediction_per_kwh:.3f}/kWh, "
                        f"Estimated total: ${total_cost:.2f}"
                    )
                
    except Exception as e:
        query_result = f"Database temporarily unavailable. I can still answer general questions!"
        print(f"⚠️ Database error: {e}")


    conversation_history.append({'role': 'user', 'content': user_input})
    

    messages = [
        {'role': 'system', 'content': 'You are an EV charging assistant. Respond in a friendly and helpful tone.'}
    ] + conversation_history[-10:] + [
        {'role': 'user', 'content': f'Additional context - Data retrieved: {query_result}'}
    ]

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages
    )
    
    reply = response.choices[0].message.content
    

    conversation_history.append({'role': 'assistant', 'content': reply})

    return reply


if __name__ == '__main__':
    print('⚡ EV Charging AI Assistant Ready! Type "exit" to quit, "clear" to reset conversation.\n')
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit']:
            print('Goodbye!')
            break
        elif user_input.lower() == 'clear':
            conversation_history.clear()
            print('🧹 Conversation cleared!\n')
            continue
            
        reply = ai_agent_query(user_input)
        print(f'🤖 Agent: {reply}\n')

