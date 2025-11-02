import streamlit as st
import pandas as pd
import joblib
from openai import OpenAI
from preprocessing import preprocess_input
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def connect_db():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        database_url = "postgresql+psycopg2://postgres:Hzz19!#%@localhost:5432/ev_charging_db"
    
    engine = create_engine(database_url)
    return engine


model = joblib.load('ev_cost_model.pkl')


st.set_page_config(page_title="⚡ EV Charging Assistant", layout="wide")


def set_bg_local(image_file):
    import base64
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        /* --- Wallpaper Background --- */
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* --- Remove Streamlit Default White Bar & Padding --- */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }}
        header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1avcm0n {{
            background: transparent !important;
            box-shadow: none !important;
        }}

        /* --- Balanced Overlay for Readability --- */
        .overlay {{
            background-color: rgba(0, 0, 0, 0.3);
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }}
        
        /* Moderate brightness boost */
        .stApp {{
            filter: brightness(1.15) !important;
        }}

        /* --- Green Buttons with Hover Effect --- */
        div.stButton > button {{
            background-color: #00CC66 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 10px !important;
            transition: 0.3s;
        }}
        div.stButton > button:hover {{
            background-color: #00FF88 !important;
            color: #000000 !important;
        }}

        /* --- Chat Bubbles --- */
        .chat-bubble-user {{
            text-align:right; 
            background-color:rgba(251, 212, 15, 0.2);
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;
            color:#FBD40F;
        }}
        .chat-bubble-ai {{
            text-align:left; 
            background-color:rgba(17, 34, 64, 0.8);
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;
            color:white;
        }}

        /* --- FIXED DROPDOWN STYLING --- */
        
        /* Closed dropdown box */
        div[data-baseweb="select"] > div {{
            background-color: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid #00CC66 !important;
            border-radius: 8px !important;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
        }}

        /* Selected value text in closed dropdown - WHITE */
        div[data-baseweb="select"] input {{
            color: #FFFFFF !important;
        }}

        /* Dropdown arrow */
        div[data-baseweb="select"] svg {{
            fill: #FFFFFF !important;
        }}

        /* Dropdown menu container - sleek bright design */
        div[role="listbox"],
        ul[role="listbox"] {{
            background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%) !important;
            border: 2px solid #00FF88 !important;
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.3), 0 0 20px rgba(0, 204, 102, 0.2) !important;
            border-radius: 12px !important;
        }}

        /* ALL dropdown menu items - sleek bright cards */
        div[role="option"],
        li[role="option"] {{
            background-color: #FAFAFA !important;
            color: #1a1a1a !important;
            padding: 12px 16px !important;
            margin: 4px 8px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            border: 1px solid #E0E0E0 !important;
        }}

        /* Selected item in dropdown - vibrant green */
        div[role="option"][aria-selected="true"],
        li[role="option"][aria-selected="true"] {{
            background: linear-gradient(135deg, #00FF88 0%, #00CC66 100%) !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border: 1px solid #00FF88 !important;
            box-shadow: 0 4px 12px rgba(0, 255, 136, 0.4) !important;
        }}

        /* Hover effect - bright and smooth */
        div[role="option"]:hover,
        li[role="option"]:hover {{
            background: linear-gradient(135deg, #E0FFE0 0%, #C0FFC0 100%) !important;
            color: #000000 !important;
            border: 1px solid #00CC66 !important;
            transform: translateX(4px) !important;
            box-shadow: 0 4px 12px rgba(0, 204, 102, 0.2) !important;
        }}

        /* --- Universal Text Colors (more specific) --- */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
            color: #FFFFFF !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }}
        
        .stApp p, .stApp label, .stApp span:not([data-baseweb]) {{
            color: #FFFFFF !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }}
        
        /* Input labels */
        .stApp label[data-testid="stWidgetLabel"] {{
            color: #FFFFFF !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }}
        
        /* Markdown text */
        .stMarkdown {{
            color: #FFFFFF !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }}

        </style>
        <div class="overlay"></div>
        """,
        unsafe_allow_html=True
    )



set_bg_local("background1.jpg")



st.markdown("<h1 style='text-align: center;'>⚡ EV Charging Cost Prediction + AI Assistant</h1>", unsafe_allow_html=True)


col1, col2 = st.columns([1.2, 0.8])


# COLUMN 1 — Prediction Section

with col1:
    st.subheader("🔋 Predict Your Charging Cost")
    st.write("Enter the charging session details below:")

    capacity = st.number_input('Battery Capacity (kWh)', min_value=10.0, step=1.0)
    duration = st.number_input('Charging duration (hours)', min_value=0.1, step=0.1)
    rate = st.number_input('Charging Rate (kW)', min_value=1.0, step=0.5)
    soc_start = st.number_input('State of Charge (Start %)', min_value=0, max_value=100, step=1)
    soc_end = st.number_input('State of Charge (End %)', min_value=0, max_value=100, step=1)
    temp = st.number_input('Temperature (°C)', min_value=-20.0, max_value=50.0, step=0.5)
    age = st.number_input('Vehicle Age (years)', min_value=0, max_value=20, step=1)
    model_choice = st.selectbox('Vehicle Model', ['Tesla Model 3', 'Hyundai Kona', 'Chevy Bolt', 'BMW i3', 'Nissan Leaf', 'Others'])
    user_type = st.selectbox('User Type', ['Commuter', 'Long-Distance Traveler', 'Casual Driver'])
    charger_type = st.selectbox('Charger Type', ['DC Fast Charger', 'Level 1', 'Level 2'])
    distance = st.number_input('Distance Driven (since last charge) (km)', min_value=0.0, step=1.0)
    energy = st.number_input('Energy Consumed (kWh)', min_value=0.1, step=0.1)

    if st.button("Predict Cost"):
        user_data = {
            "Battery Capacity (kWh)": capacity,
            "Charging Duration (hours)": duration,
            "Charging Rate (kW)": rate,
            "State of Charge (Start %)": soc_start,
            "State of Charge (End %)": soc_end,
            "Temperature (°C)": temp,
            "Vehicle Age (years)": age,
            "Vehicle Model": model_choice,
            "Charger Type": charger_type,
            "User Type": user_type,
            "Distance Driven (since last charge) (km)": distance,
            "Energy Consumed (kWh)": energy
        }

        X = preprocess_input(user_data)
        prediction = model.predict(X)[0]
        st.success(f"💰 Estimated Charging Cost: **${prediction:.2f}**")


        try:
            engine = connect_db()
            with engine.connect() as conn:
                insert_query = """
                INSERT INTO ev_predictions (
                    distance_km, energy_kwh, duration_hours, battery_capacity, charging_rate,
                    soc_start, soc_end, temperature, vehicle_age, vehicle_model,
                    charger_type, user_type, predicted_cost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = (
                    distance, energy, duration, capacity, rate,
                    soc_start, soc_end, temp, age, model_choice,
                    charger_type, user_type, float(prediction)
                )
                conn.exec_driver_sql(insert_query, data)
                conn.commit()
            st.info("✅ Prediction stored in the database successfully!")
        except Exception as e:
            st.error(f"⚠️ Database Error: {e}")


        explanation_prompt = f"""
        Explain in one paragraph why the predicted EV charging cost is ${prediction:.2f}, 
        given these parameters: duration={duration} hours, energy={energy} kWh, 
        temperature={temp}°C, vehicle age={age} years, and user type={user_type}.
        Be clear, concise, and use everyday language.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful EV assistant that explains predictions in human terms."},
                {"role": "user", "content": explanation_prompt}
            ]
        )

        ai_explanation = response.choices[0].message.content
        st.markdown(f"**🤖 Why this cost?** {ai_explanation}")



# COLUMN 2 — AI Assistant Chat

with col2:
    st.subheader("🤖 AI Assistant Chat")

    st.markdown("""
        <style>
        .chat-container {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            max-height: 450px;
            overflow-y: auto;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state["messages"][-10:]:  # show last 10
            role, content = msg["role"], msg["content"]
            if role == "user":
                st.markdown(f"<div class='chat-bubble-user'>{content}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-ai'>{content}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    with c1:
        user_input = st.text_input("💬 You:", placeholder="Ask me about your EV data or predictions...")
    with c2:
        ask = st.button("Ask")

    if st.button("🧹 Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()

    if ask and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        engine = connect_db()
        query_result = ''

        with engine.connect() as conn:
            if 'average' in user_input.lower() or 'total' in user_input.lower():
                df = pd.read_sql_query('SELECT * FROM ev_predictions;', conn)
                query_result = f"Average cost: {df['predicted_cost'].mean():.2f}, Total sessions: {len(df)}"
            elif 'predict' in user_input.lower():
                query_result = "I can provide predictions based on stored or example EV data."

        messages = [
            {"role": "system", "content": "You are a smart and friendly EV charging assistant. Keep answers short and clear."}
        ] + st.session_state["messages"][-10:] + [
            {"role": "user", "content": f"User asked: {user_input}. Data retrieved: {query_result}"}
        ]


        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        reply = response.choices[0].message.content

        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.rerun()
