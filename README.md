⚡ EV Charging AI Agent Dashboard
🧠 Overview

This project is my first personal AI Agent project that brings together Data Science, Machine Learning, and AI Assistant integration — all in one interactive web app.

The EV Charging AI Agent predicts the estimated cost of charging an electric vehicle based on user inputs and provides intelligent explanations using an OpenAI-powered chatbot.
It also stores user prediction data in a PostgreSQL database for analytics and trend tracking.

🚀 Features
🔋 EV Charging Prediction

Enter custom vehicle and charging session details

Predict the total charging cost and cost per kWh using a trained regression model

Real-time explanations of the predicted value (powered by OpenAI GPT-4o-mini)

🤖 AI Assistant Chatbot

Ask natural language questions like:

“What is the average predicted cost?”

“How many charging sessions are stored?”

“Predict cost for a Tesla Model 3”

Get intelligent summaries and insights from your data

🗄️ Database Integration

Stores all user inputs and prediction results in a PostgreSQL database (Render-hosted)

Automatically creates the table if not found

🧩 Model API (Optional)

A lightweight Flask API (app.py) is included

Accepts JSON input and returns model predictions (useful for external integrations or APIs)

🧱 Tech Stack
Layer	Technologies
Frontend / UI	Streamlit, HTML/CSS (custom styling)
Backend / AI	OpenAI API (GPT-4o-mini)
ML Model	Scikit-learn (regression model for cost prediction)
Data Handling	Pandas, Joblib, NumPy
Database	PostgreSQL (via SQLAlchemy)
Deployment	Render (Backend + Database)
Environment Management	Python-dotenv
🧠 How It Works

User Inputs Data → Capacity, duration, SoC, charger type, etc.

Preprocessing Module (preprocessing.py) transforms inputs into model-ready format.

Model (ev_cost_model.pkl) predicts cost per kWh.

Streamlit Dashboard multiplies cost × energy for total cost.

PostgreSQL Database stores the prediction (inputs + output).

OpenAI Chatbot explains the prediction in human terms or answers database questions.

🛠️ Setup & Run Locally
1. Clone the repository
git clone https://github.com/hemz19-05/ev-charging-ai-agent.git
cd ev-charging-ai-agent

2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # (Mac/Linux)
.venv\Scripts\activate         # (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Add your environment variables

Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgres_connection_url

5. Run the Streamlit app
streamlit run dashboard.py

6. (Optional) Run the Flask API
python app.py

🌐 Deployment

This project is deployed on Render, using:

render.yaml → Deployment configuration

runtime.txt → Specifies Python version (3.10.14)

.gitignore → Ensures no secret or environment files are pushed

📊 Example Prediction

Input:

Energy Consumed: 45 kWh

Duration: 3 hours

Charger Type: Level 2

Temperature: 36°C

Output:
💰 Estimated Total Charging Cost: $16.63 (≈ $0.37/kWh)

🧩 Folder Structure
EV-Charging-AI-Agent/
│
├── dashboard.py              # Main Streamlit UI
├── ai_agent.py               # AI assistant backend logic
├── ai_dashboard.py           # Chat UI for AI assistant
├── preprocessing.py          # Data preprocessing functions
├── app.py                    # Flask API (optional)
├── ev_cost_model.pkl         # Trained regression model
├── model_features.pkl        # Model feature mappings
├── requirements.txt          # Python dependencies
├── render.yaml               # Render deployment config
├── .env                      # Environment variables (local only)
├── .gitignore                # Ignored files
└── README.md                 # Project documentation



💡 Future Improvements

-Add user authentication for personalized dashboards

-Visualize prediction history directly in the dashboard

-Deploy the AI Assistant as an API endpoint (for web/mobile apps)

-Integrate LangChain for conversational memory

*This repository is for learning and portfolio demonstration only.Reuse of code is not permitted without permission.

👩‍💻 Author

Hema Kandivan
🎓 MSc Data Science @ Universiti Teknologi PETRONAS, Malaysia
💡 Passionate about AI Agents, LLMs, and Applied Data Science
