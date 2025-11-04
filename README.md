# ⚡ EV Charging AI Agent Dashboard  

### 🧠 Overview  
This project is my **first personal AI Agent project** that brings together **Data Science, Machine Learning, and AI Assistant integration** — all in one interactive web app.  

The **EV Charging AI Agent** predicts the **estimated cost of charging** an electric vehicle based on user inputs and provides intelligent explanations using an **OpenAI-powered chatbot**.  
It also stores user prediction data in a **PostgreSQL database** for analytics and trend tracking.  

---

## 🚀 Features  

### 🔋 EV Charging Prediction  
- Enter custom vehicle and charging session details  
- Predict the **total charging cost** and **cost per kWh** using a trained regression model  
- Real-time explanations of the predicted value (powered by OpenAI GPT-4o-mini)  

### 🤖 AI Assistant Chatbot  
- Ask natural language questions like:  
  - “What is the average predicted cost?”  
  - “How many charging sessions are stored?”  
  - “Predict cost for a Tesla Model 3”  
- Get intelligent summaries and insights from your data  

### 🗄️ Database Integration  
- Stores all user inputs and prediction results in a **PostgreSQL database** (Render-hosted)  
- Automatically creates the table if not found  

### 🧩 Model API (Optional)  
- A lightweight **Flask API (`app.py`)** is included  
- Accepts JSON input and returns model predictions (useful for external integrations or APIs)  

---

## 🧱 Tech Stack  

| Layer | Technologies |
|-------|---------------|
| **Frontend / UI** | Streamlit, HTML/CSS (custom styling) |
| **Backend / AI** | OpenAI API (GPT-4o-mini) |
| **ML Model** | Scikit-learn (Regression model for cost prediction) |
| **Data Handling** | Pandas, Joblib, NumPy |
| **Database** | PostgreSQL (via SQLAlchemy) |
| **Deployment** | Render (Backend + Database) |
| **Environment Management** | Python-dotenv |

---

## 🧠 How It Works  

1. **User Inputs Data** → Battery capacity, duration, SoC, charger type, etc.  
2. **Preprocessing Module (`preprocessing.py`)** transforms inputs into model-ready format.  
3. **Model (`ev_cost_model.pkl`)** predicts **cost per kWh**.  
4. **Streamlit Dashboard** multiplies cost × energy for **total cost**.  
5. **PostgreSQL Database** stores the prediction (inputs + output).  
6. **OpenAI Chatbot** explains the prediction in human terms or answers database questions.  

---

## 🛠️ Setup & Run Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/hemz19-05/ev-charging-ai-agent.git
cd ev-charging-ai-agent


## This repository is for learning and portfolio demonstration only.Reuse of code is not permitted without permission.

##👩‍💻 Author

Hema Kandivan
🎓 MSc Data Science @ Universiti Teknologi PETRONAS, Malaysia
💡 Passionate about AI Agents, LLMs, and Applied Data Science
