import streamlit as st
import pandas as pd
import joblib
from openai import OpenAI
from preprocessing import preprocess_input
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

st.set_page_config(page_title="⚡ EV Charging AI Assistant", page_icon="⚡")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


if "ai_messages" not in st.session_state:
    st.session_state["ai_messages"] = []

@st.cache_resource
def get_engine():
    """Create and cache the SQLAlchemy engine."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        st.warning("⚠️ DATABASE_URL not found in environment variables.")
        return None
    return create_engine(database_url)

@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the trained cost prediction model."""
    return joblib.load('ev_cost_model.pkl')

model = load_model()


st.title("⚡ EV Charging AI Assistant")

st.markdown("""
This intelligent assistant can:
- 💬 Answer questions about your EV charging database  
- 🔍 Summarize patterns and statistics  
- ⚙️ Predict charging cost for sample EV configurations  

**Try asking:**
- "What is the average predicted cost?"
- "How many sessions are stored?"
- "Predict cost for a Tesla Model 3"
""")


st.subheader("💬 Conversation")
for msg in st.session_state["ai_messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Assistant:** {msg['content']}")


if st.button("🧹 Clear Conversation"):
    st.session_state["ai_messages"] = []
    st.rerun()


user_input = st.text_input("You:", placeholder="Ask me something about EV charging...", key="user_input_field")

if user_input:
    # Add user message to history
    st.session_state["ai_messages"].append({"role": "user", "content": user_input})
    
    query_result = ''
    
    try:
        engine = get_engine()

        if engine:
            with engine.connect() as conn:
                if 'average' in user_input.lower() or 'total' in user_input.lower():
                    df = pd.read_sql_query('SELECT * FROM ev_predictions;', conn)
                    if not df.empty:
                        query_result = f"Average cost: ${df['predicted_cost'].mean():.2f}, Total sessions: {len(df)}"
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
                    st.success(f"💰 Estimated Total Charging Cost: **${total_cost:.2f}** (≈ ${prediction_per_kwh:.3f}/kWh)")

        else:
            query_result = 'Database connection not configured.' 

    except Exception as e:
        query_result = "Database temporarily unavailable. I can still answer general questions about EV charging!"
        st.warning(f"⚠️ Database connection issue")

    # Create messages for OpenAI with conversation history
    with st.spinner("🤖 Thinking..."):
        messages = [
            {"role": "system", "content": "You are an EV charging assistant that explains data in a friendly, helpful way."}
        ] + st.session_state["ai_messages"][-10:] + [  # Keep last 10 messages for context
            {"role": "user", "content": f"Additional context - Data retrieved: {query_result}"}
        ]
        
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        reply = response.choices[0].message.content
    
    st.session_state["ai_messages"].append({"role": "assistant", "content": reply})
    


