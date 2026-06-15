import streamlit as st
import requests  # This library lets Streamlit talk to your FastAPI backend

# ==========================================
# 1. SET UP PAGE CONFIGURATION & VIBRANT STYLING
# ==========================================
st.set_page_config(
    page_title="Heart Disease Prediction Engine",
    page_icon="❤️",
    layout="centered"
)

st.html("""
    <style>
    .stApp {
        background: radial-gradient(circle, rgba(255,240,242,1) 0%, rgba(255,255,255,1) 100%);
    }
    .main-title {
        color: #C2185B !important;
        font-weight: 800;
        text-align: center;
    }
    .healthy-card {
        background-color: #E8F5E9;
        border-left: 6px solid #2E7D32;
        padding: 20px;
        border-radius: 8px;
        color: #1B5E20;
    }
    .at-risk-card {
        background-color: #FFEBEE;
        border-left: 6px solid #C62828;
        padding: 20px;
        border-radius: 8px;
        color: #B71C1C;
    }
    </style>
""")

st.html("<h1 class='main-title'>❤️ Heart Disease Diagnostic Assistant</h1>")
st.write("---")

# ==========================================
# 2. INTERACTIVE USER INTERFACE DESIGN
# ==========================================
st.subheader("📋 Enter Patient Clinical Parameters")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=54, step=1)
    sex_label = st.selectbox("Sex", options=["Male", "Female"], index=0)
    sex = "M" if sex_label == "Male" else "F"
    chest_pain_type = st.selectbox("Chest Pain Type", options=["ASY", "NAP", "ATA", "TA"], index=0)
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120, step=1)
    cholesterol = st.number_input("Serum Cholesterol (mg/dL)", min_value=0, max_value=600, value=240, step=1)
    fasting_bs_label = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=["No", "Yes"], index=0)
    fasting_bs = 1 if fasting_bs_label == "Yes" else 0

with col2:
    resting_ecg = st.selectbox("Resting ECG Results", options=["Normal", "ST", "LVH"], index=0)
    max_hr = st.number_input("Maximum Heart Rate Achieved (MaxHR)", min_value=50, max_value=250, value=150, step=1)
    exercise_angina_label = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"], index=0)
    exercise_angina = "Y" if exercise_angina_label == "Yes" else "N"
    oldpeak = st.number_input("ST Depression Induced by Exercise (Oldpeak)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
    st_slope = st.selectbox("Slope of Peak Exercise ST Segment (ST_Slope)", options=["Up", "Flat", "Down"], index=0)

st.markdown("---")

# ==========================================
# 3. COMMUNICATING WITH YOUR FASTAPI BACKEND
# ==========================================
if st.button("Generate Diagnostic Evaluation", type="primary", use_container_width=True):
    
    # Package the raw inputs to match your FastAPI Pydantic input schema fields exactly
    payload = {
        "Age": age,
        "Sex": sex,
        "ChestPain": chest_pain_type,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "RestingECG": resting_ecg,
        "MaxHR": max_hr,  
        "ExerciseAngina": exercise_angina,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope
    }
    
    # Define your live local FastAPI endpoint URL
    FASTAPI_URL = "https://heart-health-backend-vklk.onrender.com"
    
    try:
        # Send the payload via a POST request straight to your running FastAPI server
        response = requests.post(FASTAPI_URL, json=payload)
        
        if response.status_code == 200:
            # Extract the processed output, probability, and custom message from your FastAPI response
            result = response.json()
            raw_prediction = result["prediction"]
            api_message = result["message"]
            
            # ==========================================
            # 4. RENDER VIBRANT DIAGNOSTIC RESULTS
            # ==========================================
            st.write("### 📊 Diagnostic Summary")
            
            if raw_prediction == 1:
                st.html(f"""
                    <div class="at-risk-card">
                        <h3>⚠️ High Risk Flagged (Status: {raw_prediction})</h3>
                        <p>{api_message}</p>
                    </div>
                """)
            else:
                st.html(f"""
                    <div class="healthy-card">
                        <h3>✅ Low Risk Flagged (Status: {raw_prediction})</h3>
                        <p>{api_message}</p>
                    </div>
                """)
        else:
            st.error(f"Backend API returned an error code: {response.status_code}")
            st.info(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the Backend server.")
        st.info("Make sure your FastAPI server is currently running in your second terminal tab using the `python -m uvicorn ...` command!")
